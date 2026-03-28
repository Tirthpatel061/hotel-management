"""Monthly salary calculation from attendance."""
from calendar import monthrange
from datetime import date
from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import and_

from extensions import db
from models.entities import Attendance, SalaryRecord, Staff, working_days_in_month
from utils.decorators import roles_required

bp = Blueprint("salary", __name__)


def _compute_for_staff(staff: Staff, month_year: str) -> SalaryRecord:
    year, month = map(int, month_year.split("-"))
    first = date(year, month, 1)
    last_d = monthrange(year, month)[1]
    last = date(year, month, last_d)

    present = (
        Attendance.query.filter(
            and_(
                Attendance.staff_id == staff.staff_id,
                Attendance.att_date >= first,
                Attendance.att_date <= last,
                Attendance.status == "present",
            )
        ).count()
    )

    wd = working_days_in_month(year, month)
    base = Decimal(str(staff.salary))
    per_day = base / Decimal(wd)
    total = (per_day * Decimal(present)).quantize(Decimal("0.01"))

    rec = SalaryRecord.query.filter_by(staff_id=staff.staff_id, month_year=month_year).first()
    if rec:
        rec.base_salary = base
        rec.present_days = present
        rec.working_days = wd
        rec.total_salary = total
    else:
        rec = SalaryRecord(
            staff_id=staff.staff_id,
            month_year=month_year,
            base_salary=base,
            present_days=present,
            working_days=wd,
            total_salary=total,
            payment_status="Pending",
        )
        db.session.add(rec)
    return rec


@bp.route("/", methods=["GET", "POST"])
@login_required
@roles_required("admin", "manager")
def page():
    month_year = request.values.get("month_year") or date.today().strftime("%Y-%m")

    if request.method == "POST" and request.form.get("action") == "compute":
        staff_list = Staff.query.filter_by(is_active=True).all()
        for s in staff_list:
            _compute_for_staff(s, month_year)
        db.session.commit()
        flash(f"Salary computed for {month_year}.", "success")
        return redirect(url_for("salary.page", month_year=month_year))

    records = (
        SalaryRecord.query.filter_by(month_year=month_year)
        .order_by(SalaryRecord.staff_id)
        .all()
    )

    return render_template("salary.html", month_year=month_year, records=records)


@bp.route("/pay/<int:salary_id>", methods=["POST"])
@login_required
@roles_required("admin", "manager")
def mark_paid(salary_id):
    rec = SalaryRecord.query.get_or_404(salary_id)
    rec.payment_status = "Paid"
    db.session.commit()
    flash("Salary marked as paid.", "success")
    return redirect(url_for("salary.page", month_year=rec.month_year))
