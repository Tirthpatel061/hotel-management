"""Staff CRUD."""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from extensions import db
from models.entities import Staff, User
from utils.decorators import roles_required

bp = Blueprint("staff", __name__)


@bp.route("/")
@login_required
@roles_required("admin", "manager")
def list_staff():
    rows = Staff.query.order_by(Staff.name).all()
    return render_template("staff.html", staff_list=rows)


@bp.route("/add", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def add_staff():
    name = request.form.get("name", "").strip()
    role = request.form.get("role", "Waiter")
    phone = request.form.get("phone", "").strip()
    salary = request.form.get("salary", type=float) or 0
    joining = request.form.get("joining_date")
    if not name or not phone or not joining:
        flash("Name, phone, and joining date are required.", "warning")
        return redirect(url_for("staff.list_staff"))
    try:
        jd = datetime.strptime(joining, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid joining date.", "danger")
        return redirect(url_for("staff.list_staff"))
    db.session.add(
        Staff(name=name, role=role, phone=phone, salary=salary, joining_date=jd)
    )
    db.session.commit()
    flash("Staff member added.", "success")
    return redirect(url_for("staff.list_staff"))


@bp.route("/edit/<int:staff_id>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def edit_staff(staff_id):
    s = Staff.query.get_or_404(staff_id)
    s.name = request.form.get("name", "").strip() or s.name
    s.role = request.form.get("role", s.role)
    s.phone = request.form.get("phone", "").strip() or s.phone
    s.salary = request.form.get("salary", type=float) or s.salary
    joining = request.form.get("joining_date")
    if joining:
        try:
            s.joining_date = datetime.strptime(joining, "%Y-%m-%d").date()
        except ValueError:
            pass
    s.is_active = request.form.get("is_active") == "on"
    db.session.commit()
    flash("Staff updated.", "success")
    return redirect(url_for("staff.list_staff"))


@bp.route("/delete/<int:staff_id>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def delete_staff(staff_id):
    s = Staff.query.get_or_404(staff_id)
    for u in User.query.filter_by(staff_id=staff_id).all():
        u.staff_id = None
    db.session.delete(s)
    db.session.commit()
    flash("Staff removed.", "info")
    return redirect(url_for("staff.list_staff"))
