"""Sales and operational reports."""
from calendar import monthrange
from datetime import date, datetime

from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func

from extensions import db
from models.entities import Bill, MenuItem, Order, OrderItem
from utils.decorators import roles_required

bp = Blueprint("reports", __name__)


@bp.route("/")
@login_required
@roles_required("admin", "manager")
def page():
    today = date.today()
    month_str = request.args.get("month") or today.strftime("%Y-%m")
    year, month = map(int, month_str.split("-"))
    first = datetime.combine(date(year, month, 1), datetime.min.time())
    last_d = monthrange(year, month)[1]
    last = datetime.combine(date(year, month, last_d), datetime.max.time())

    daily_start = datetime.combine(today, datetime.min.time())
    daily_end = datetime.combine(today, datetime.max.time())

    daily_sales = (
        db.session.query(func.coalesce(func.sum(Bill.total_amount), 0))
        .filter(
            Bill.payment_status == "Paid",
            Bill.created_at >= daily_start,
            Bill.created_at <= daily_end,
        )
        .scalar()
    )

    monthly_sales = (
        db.session.query(func.coalesce(func.sum(Bill.total_amount), 0))
        .filter(
            Bill.payment_status == "Paid",
            Bill.created_at >= first,
            Bill.created_at <= last,
        )
        .scalar()
    )

    table_cnt = Order.query.filter(
        Order.order_type == "table",
        Order.order_time >= first,
        Order.order_time <= last,
    ).count()
    parcel_cnt = Order.query.filter(
        Order.order_type == "parcel",
        Order.order_time >= first,
        Order.order_time <= last,
    ).count()

    top_items = (
        db.session.query(
            OrderItem.item_id,
            func.sum(OrderItem.quantity).label("qty"),
        )
        .join(Order, Order.order_id == OrderItem.order_id)
        .filter(Order.order_time >= first, Order.order_time <= last)
        .group_by(OrderItem.item_id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(10)
        .all()
    )

    top_rows = []
    for item_id, qty in top_items:
        m = MenuItem.query.get(item_id)
        top_rows.append({"name": m.name if m else str(item_id), "qty": int(qty)})

    return render_template(
        "reports.html",
        month_str=month_str,
        daily_sales=float(daily_sales or 0),
        monthly_sales=float(monthly_sales or 0),
        table_cnt=table_cnt,
        parcel_cnt=parcel_cnt,
        top_rows=top_rows,
    )
