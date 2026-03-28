"""Bill generation with optional GST."""
from decimal import Decimal

from flask import current_app

from extensions import db
from models.entities import Bill, MenuItem, Order, OrderItem


def order_subtotal(order: Order) -> Decimal:
    total = Decimal("0")
    for line in order.items:
        total += Decimal(str(line.price)) * int(line.quantity)
    return total.quantize(Decimal("0.01"))


def compute_gst(subtotal: Decimal, gst_percent: float) -> Decimal:
    return (subtotal * Decimal(str(gst_percent)) / Decimal("100")).quantize(Decimal("0.01"))


def create_or_update_bill(order: Order) -> Bill:
    """Create bill from order lines; applies GST from app config."""
    subtotal = order_subtotal(order)
    gst_pct = float(current_app.config.get("GST_PERCENT", 5))
    gst = compute_gst(subtotal, gst_pct)
    total = (subtotal + gst).quantize(Decimal("0.01"))

    bill = Bill.query.filter_by(order_id=order.order_id).first()
    if bill:
        bill.subtotal = subtotal
        bill.gst_amount = gst
        bill.total_amount = total
    else:
        bill = Bill(
            order_id=order.order_id,
            subtotal=subtotal,
            gst_amount=gst,
            total_amount=total,
            payment_status="Pending",
            payment_method="Cash",
        )
        db.session.add(bill)
    return bill


def finalize_order_for_billing(order: Order) -> None:
    """When table Served or parcel Delivered, ensure bill exists."""
    create_or_update_bill(order)
