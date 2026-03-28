"""SQLAlchemy models (database tables)."""
from datetime import date
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class Staff(db.Model):
    __tablename__ = "staff"

    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum("Waiter", "Chef", "Manager", "Other", name="staff_role"), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    joining_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    users = db.relationship("User", backref="staff_member", lazy=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("admin", "manager", "waiter", "chef", name="user_role"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class DiningTable(db.Model):
    __tablename__ = "tables"

    table_id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(
        db.Enum("Available", "Occupied", "Cleaning", name="table_status"),
        nullable=False,
        default="Available",
    )


class MenuItem(db.Model):
    __tablename__ = "menu_items"

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)


class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.table_id"), nullable=True)
    parcel_customer_name = db.Column(db.String(120), nullable=True)
    parcel_phone = db.Column(db.String(20), nullable=True)
    order_time = db.Column(db.DateTime, server_default=db.func.now())
    order_type = db.Column(
        db.Enum("table", "parcel", name="order_type_enum"),
        nullable=False,
        default="table",
    )
    status = db.Column(
        db.Enum("Pending", "Preparing", "Ready", "Served", "Delivered", name="order_status_enum"),
        nullable=False,
        default="Pending",
    )

    table = db.relationship("DiningTable", backref="orders", lazy=True)
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_items.item_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    menu_item = db.relationship("MenuItem", lazy=True)


class Bill(db.Model):
    __tablename__ = "bills"

    bill_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), unique=True, nullable=False)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)
    gst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    payment_status = db.Column(
        db.Enum("Pending", "Paid", name="bill_payment_status"),
        nullable=False,
        default="Pending",
    )
    payment_method = db.Column(
        db.Enum("Cash", "Card", "UPI", "Other", name="payment_method_enum"),
        nullable=False,
        default="Cash",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    order = db.relationship("Order", backref=db.backref("bill", uselist=False), lazy=True)


class Attendance(db.Model):
    __tablename__ = "attendance"

    attendance_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"), nullable=False)
    att_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum("present", "absent", name="att_status"), nullable=False, default="present")

    staff = db.relationship("Staff", backref="attendance_records", lazy=True)

    __table_args__ = (db.UniqueConstraint("staff_id", "att_date", name="uq_staff_date"),)


class SalaryRecord(db.Model):
    __tablename__ = "salary_records"

    salary_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"), nullable=False)
    month_year = db.Column(db.String(7), nullable=False)  # YYYY-MM
    base_salary = db.Column(db.Numeric(12, 2), nullable=False)
    present_days = db.Column(db.Integer, nullable=False)
    working_days = db.Column(db.Integer, nullable=False)
    total_salary = db.Column(db.Numeric(12, 2), nullable=False)
    payment_status = db.Column(
        db.Enum("Pending", "Paid", name="salary_payment_status"),
        nullable=False,
        default="Pending",
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    staff = db.relationship("Staff", backref="salary_records", lazy=True)

    __table_args__ = (db.UniqueConstraint("staff_id", "month_year", name="uq_staff_month"),)


def working_days_in_month(year: int, month: int) -> int:
    """Approximate working days (Mon–Sat) in a calendar month."""
    import calendar

    count = 0
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        wd = date(year, month, day).weekday()
        if wd < 6:
            count += 1
    return count or 1
