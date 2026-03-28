"""Menu CRUD (admin / manager)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from models.entities import MenuItem
from utils.decorators import roles_required

bp = Blueprint("menu", __name__)


@bp.route("/")
@login_required
@roles_required("admin", "manager")
def list_menu():
    items = MenuItem.query.order_by(MenuItem.category, MenuItem.name).all()
    return render_template("menu.html", items=items)


@bp.route("/add", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def add_item():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    price = request.form.get("price", type=float)
    availability = request.form.get("availability") == "on"
    if not name or not category or price is None:
        flash("Name, category, and price are required.", "warning")
        return redirect(url_for("menu.list_menu"))
    if MenuItem.query.filter_by(name=name).first():
        flash("An item with this name already exists.", "danger")
        return redirect(url_for("menu.list_menu"))
    db.session.add(
        MenuItem(name=name, category=category, price=price, availability=availability)
    )
    db.session.commit()
    flash("Menu item added.", "success")
    return redirect(url_for("menu.list_menu"))


@bp.route("/edit/<int:item_id>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def edit_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    price = request.form.get("price", type=float)
    availability = request.form.get("availability") == "on"
    if not name or not category or price is None:
        flash("Invalid data.", "warning")
        return redirect(url_for("menu.list_menu"))
    other = MenuItem.query.filter(MenuItem.name == name, MenuItem.item_id != item_id).first()
    if other:
        flash("Another item already uses this name.", "danger")
        return redirect(url_for("menu.list_menu"))
    item.name = name
    item.category = category
    item.price = price
    item.availability = availability
    db.session.commit()
    flash("Menu item updated.", "success")
    return redirect(url_for("menu.list_menu"))


@bp.route("/delete/<int:item_id>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def delete_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Menu item deleted.", "info")
    return redirect(url_for("menu.list_menu"))
