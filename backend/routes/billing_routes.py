"""Billing list, receipt view, mark paid."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.orm import joinedload

from extensions import db
from models.entities import Bill, Order, OrderItem
from services.billing_service import create_or_update_bill

bp = Blueprint("billing", __name__)


@bp.route("/")
@login_required
def list_bills():
    bills = (
        Bill.query.options(joinedload(Bill.order))
        .order_by(Bill.created_at.desc())
        .all()
    )
    return render_template("billing.html", bills=bills)


@bp.route("/receipt/<int:bill_id>")
@login_required
def receipt(bill_id):
    bill = (
        Bill.query.options(
            joinedload(Bill.order).joinedload(Order.items).joinedload(OrderItem.menu_item),
            joinedload(Bill.order).joinedload(Order.table),
        )
        .get_or_404(bill_id)
    )
    order = bill.order
    return render_template("receipt.html", bill=bill, order=order)


@bp.route("/regenerate/<int:order_id>", methods=["POST"])
@login_required
def regenerate(order_id):
    order = Order.query.get_or_404(order_id)
    create_or_update_bill(order)
    db.session.commit()
    flash("Bill totals refreshed.", "success")
    return redirect(url_for("billing.list_bills"))


@bp.route("/pay/<int:bill_id>", methods=["POST"])
@login_required
def mark_paid(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    bill.payment_status = "Paid"
    method = request.form.get("payment_method", "Cash")
    if method in ("Cash", "Card", "UPI", "Other"):
        bill.payment_method = method
    db.session.commit()
    flash("Payment recorded.", "success")
    return redirect(url_for("billing.receipt", bill_id=bill_id))
