"""Daily attendance marking and history."""
from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import and_

from extensions import db
from models.entities import Attendance, Staff
from utils.decorators import roles_required

bp = Blueprint("attendance", __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
@roles_required("admin", "manager")
def page():
    att_date_str = request.values.get("att_date") or date.today().isoformat()
    try:
        att_date = datetime.strptime(att_date_str, "%Y-%m-%d").date()
    except ValueError:
        att_date = date.today()

    staff_rows = Staff.query.filter_by(is_active=True).order_by(Staff.name).all()

    if request.method == "POST":
        for s in staff_rows:
            key = f"status_{s.staff_id}"
            status = request.form.get(key, "absent")
            if status not in ("present", "absent"):
                status = "absent"
            rec = Attendance.query.filter(
                and_(Attendance.staff_id == s.staff_id, Attendance.att_date == att_date)
            ).first()
            if rec:
                rec.status = status
            else:
                db.session.add(
                    Attendance(staff_id=s.staff_id, att_date=att_date, status=status)
                )
        db.session.commit()
        flash(f"Attendance saved for {att_date}.", "success")
        return redirect(url_for("attendance.page", att_date=att_date.isoformat()))

    # Load current statuses for display
    records = {
        r.staff_id: r.status
        for r in Attendance.query.filter(Attendance.att_date == att_date).all()
    }

    # History: last 30 rows
    history = (
        Attendance.query.order_by(Attendance.att_date.desc(), Attendance.staff_id)
        .limit(60)
        .all()
    )

    return render_template(
        "attendance.html",
        att_date=att_date,
        staff_rows=staff_rows,
        records=records,
        history=history,
    )
