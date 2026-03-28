"""Kitchen dashboard: view and update order status."""
from typing import Optional

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from sqlalchemy.orm import joinedload

from extensions import db
from models.entities import DiningTable, Order, OrderItem
from services.billing_service import finalize_order_for_billing

bp = Blueprint("kitchen", __name__)


def _next_status(order: Order) -> Optional[str]:
    s = order.status
    if s == "Pending":
        return "Preparing"
    if s == "Preparing":
        return "Ready"
    if s == "Ready":
        return "Served" if order.order_type == "table" else "Delivered"
    return None


@bp.route("/")
@login_required
def board():
    orders = (
        Order.query.options(
            joinedload(Order.items).joinedload(OrderItem.menu_item),
            joinedload(Order.table),
        )
        .filter(~Order.status.in_(["Served", "Delivered"]))
        .order_by(Order.order_time.asc())
        .all()
    )
    return render_template("kitchen.html", orders=orders)


@bp.route("/status/<int:order_id>", methods=["POST"])
@login_required
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    nxt = _next_status(order)
    if not nxt:
        flash("Order is already completed.", "info")
        return redirect(url_for("kitchen.board"))

    order.status = nxt
    if nxt in ("Served", "Delivered"):
        finalize_order_for_billing(order)
        if order.order_type == "table" and order.table_id:
            t = DiningTable.query.get(order.table_id)
            if t:
                t.status = "Available"
    db.session.commit()
    flash(f"Order #{order_id} updated to {nxt}.", "success")
    return redirect(url_for("kitchen.board"))
