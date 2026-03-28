"""Main dashboard with KPI cards."""
from datetime import date, datetime

from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from extensions import db
from models.entities import Attendance, Bill, DiningTable, Order, Staff

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    total_tables = db.session.query(func.count(DiningTable.table_id)).scalar() or 0

    active_orders = (
        Order.query.filter(~Order.status.in_(["Served", "Delivered"])).count()
    )

    parcel_today = (
        Order.query.filter(
            Order.order_type == "parcel",
            Order.order_time >= start,
            Order.order_time <= end,
        ).count()
    )

    daily_revenue = (
        db.session.query(func.coalesce(func.sum(Bill.total_amount), 0))
        .filter(
            Bill.payment_status == "Paid",
            Bill.created_at >= start,
            Bill.created_at <= end,
        )
        .scalar()
    )
    daily_revenue = float(daily_revenue or 0)

    staff_present = (
        db.session.query(func.count(Attendance.attendance_id))
        .filter(Attendance.att_date == today, Attendance.status == "present")
        .scalar()
        or 0
    )

    total_staff = (
        db.session.query(func.count(Staff.staff_id)).filter(Staff.is_active.is_(True)).scalar() or 0
    )

    return render_template(
        "dashboard.html",
        total_tables=total_tables,
        active_orders=active_orders,
        parcel_today=parcel_today,
        daily_revenue=daily_revenue,
        staff_present=staff_present,
        total_staff=total_staff,
    )
