"""Table orders and parcel / takeaway orders."""
import json

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.orm import joinedload

from extensions import db
from models.entities import DiningTable, MenuItem, Order, OrderItem

bp = Blueprint("orders", __name__)


def _parse_items_from_form():
    """Expect JSON string in 'items' field: [{\"item_id\":1,\"quantity\":2}, ...]"""
    raw = request.form.get("items_json", "[]")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    out = []
    for row in data:
        try:
            iid = int(row.get("item_id"))
            qty = int(row.get("quantity", 0))
            if qty > 0:
                out.append({"item_id": iid, "quantity": qty})
        except (TypeError, ValueError):
            continue
    return out


def _create_order_lines(order: Order, items_payload):
    for row in items_payload:
        menu = MenuItem.query.get(row["item_id"])
        if not menu or not menu.availability:
            raise ValueError(f"Item {row['item_id']} is not available.")
        db.session.add(
            OrderItem(
                order_id=order.order_id,
                item_id=menu.item_id,
                quantity=row["quantity"],
                price=menu.price,
            )
        )


def _append_order_lines(order: Order, items_payload):
    """Add items to an existing order; merge quantity if same menu item already on ticket."""
    for row in items_payload:
        menu = MenuItem.query.get(row["item_id"])
        if not menu or not menu.availability:
            raise ValueError(f"Item {row['item_id']} is not available.")
        line = OrderItem.query.filter_by(
            order_id=order.order_id, item_id=menu.item_id
        ).first()
        if line:
            line.quantity = int(line.quantity) + int(row["quantity"])
        else:
            db.session.add(
                OrderItem(
                    order_id=order.order_id,
                    item_id=menu.item_id,
                    quantity=row["quantity"],
                    price=menu.price,
                )
            )


@bp.route("/table", methods=["GET", "POST"])
@login_required
def table_orders():
    tables = DiningTable.query.order_by(DiningTable.table_number).all()
    menu = (
        MenuItem.query.filter_by(availability=True)
        .order_by(MenuItem.category, MenuItem.name)
        .all()
    )

    active_orders = Order.query.filter(
        Order.order_type == "table",
        ~Order.status.in_(["Served", "Delivered"]),
    ).all()
    active_by_table = {o.table_id: o.order_id for o in active_orders}

    if request.method == "POST":
        table_id = request.form.get("table_id", type=int)
        items_payload = _parse_items_from_form()
        if not table_id or not items_payload:
            flash("Select a table and at least one item.", "warning")
            return redirect(url_for("orders.table_orders"))

        table = DiningTable.query.get(table_id)
        if not table:
            flash("Invalid table.", "danger")
            return redirect(url_for("orders.table_orders"))

        existing = (
            Order.query.filter(
                Order.table_id == table_id,
                Order.order_type == "table",
                ~Order.status.in_(["Served", "Delivered"]),
            )
            .first()
        )

        # Add more items to an open table order: save only (no kitchen re-print).
        if existing:
            try:
                _append_order_lines(existing, items_payload)
            except ValueError as e:
                db.session.rollback()
                flash(str(e), "danger")
                return redirect(url_for("orders.table_orders"))

            db.session.commit()
            flash(
                f"Items saved to order #{existing.order_id} for {table.table_number}. "
                "Kitchen ticket is not re-printed. Print the final bill from Billing when the meal is complete.",
                "success",
            )
            return redirect(url_for("orders.table_orders"))

        # First submission for this table: new order, then auto-open kitchen ticket print.
        order = Order(
            table_id=table_id,
            order_type="table",
            status="Pending",
        )
        db.session.add(order)
        db.session.flush()
        try:
            _create_order_lines(order, items_payload)
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "danger")
            return redirect(url_for("orders.table_orders"))

        table.status = "Occupied"
        db.session.commit()
        flash(
            f"Order #{order.order_id} sent to kitchen — printing ticket now.",
            "success",
        )
        return redirect(url_for("orders.kitchen_ticket", order_id=order.order_id))

    return render_template(
        "table_orders.html",
        tables=tables,
        menu=menu,
        active_by_table=active_by_table,
    )


@bp.route("/kot/<int:order_id>")
@login_required
def kitchen_ticket(order_id):
    """Kitchen order ticket (KOT) — auto-print in browser for new table orders."""
    order = (
        Order.query.options(
            joinedload(Order.items).joinedload(OrderItem.menu_item),
            joinedload(Order.table),
        )
        .filter_by(order_id=order_id, order_type="table")
        .first()
    )
    if not order:
        abort(404)
    return render_template("kitchen_ticket.html", order=order)


@bp.route("/parcel", methods=["GET", "POST"])
@login_required
def parcel_orders():
    menu = (
        MenuItem.query.filter_by(availability=True)
        .order_by(MenuItem.category, MenuItem.name)
        .all()
    )

    if request.method == "POST":
        name = request.form.get("customer_name", "").strip()
        phone = request.form.get("customer_phone", "").strip()
        items_payload = _parse_items_from_form()
        if not name or not phone or not items_payload:
            flash("Customer name, phone, and at least one item are required.", "warning")
            return redirect(url_for("orders.parcel_orders"))

        order = Order(
            table_id=None,
            parcel_customer_name=name,
            parcel_phone=phone,
            order_type="parcel",
            status="Pending",
        )
        db.session.add(order)
        db.session.flush()
        try:
            _create_order_lines(order, items_payload)
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "danger")
            return redirect(url_for("orders.parcel_orders"))

        db.session.commit()
        flash(f"Parcel order #{order.order_id} created.", "success")
        return redirect(url_for("orders.parcel_orders"))

    return render_template("parcel_orders.html", menu=menu)
