# -*- coding: utf-8 -*-
"""
app/routes/employee.py
Routes quản lý nhân viên: thêm, sửa, xóa, tìm kiếm.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.extensions import db, VI_TRI_MAP, TRINH_DO_LIST
from app.models import Employee
from app.services.helpers import normalize_text
from app.services.validation import validate_employee_payload

bp = Blueprint("employee", __name__)


@bp.route("/employees")
@login_required
def employees_page():
    q = request.args.get("q", "").strip()
    query = Employee.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Employee.ma_nv.ilike(like),
                Employee.ho_ten.ilike(like),
                Employee.email.ilike(like),
                Employee.bo_phan.ilike(like),
                Employee.vi_tri.ilike(like),
            )
        )
    employees = query.order_by(Employee.id.desc()).all()
    return render_template(
        "employee/employees.html",
        employees=employees,
        q=q,
        vi_tri_map=VI_TRI_MAP,
        trinh_do_list=TRINH_DO_LIST
    )


@bp.route("/employees/add", methods=["POST"])
@login_required
def employee_add():
    payload = {
        "ma_nv": normalize_text(request.form.get("ma_nv")),
        "ho_ten": normalize_text(request.form.get("ho_ten")),
        "email": normalize_text(request.form.get("email")),
        "bo_phan": normalize_text(request.form.get("bo_phan")),
        "vi_tri": normalize_text(request.form.get("vi_tri")),
    }
    errors = validate_employee_payload(payload)
    if errors:
        flash("; ".join(errors), "danger")
        return redirect(url_for("employee.employees_page"))
    if Employee.query.filter_by(ma_nv=payload["ma_nv"]).first():
        flash(f"Mã nhân viên '{payload['ma_nv']}' đã tồn tại.", "danger")
        return redirect(url_for("employee.employees_page"))

    emp = Employee(
        ma_nv=payload["ma_nv"],
        ho_ten=payload["ho_ten"],
        email=payload["email"],
        bo_phan=payload["bo_phan"],
        vi_tri=payload["vi_tri"],
        created_by_id=current_user.id,
        updated_by_id=current_user.id
    )
    db.session.add(emp)
    db.session.commit()
    flash(f"Đã thêm nhân viên '{payload['ho_ten']}' thành công.", "success")
    return redirect(url_for("employee.employees_page"))


@bp.route("/employees/edit/<int:emp_id>", methods=["POST"])
@login_required
def employee_edit(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    payload = {
        "ma_nv": normalize_text(request.form.get("ma_nv")),
        "ho_ten": normalize_text(request.form.get("ho_ten")),
        "email": normalize_text(request.form.get("email")),
        "bo_phan": normalize_text(request.form.get("bo_phan")),
        "vi_tri": normalize_text(request.form.get("vi_tri")),
    }
    errors = validate_employee_payload(payload)
    if errors:
        flash("; ".join(errors), "danger")
        return redirect(url_for("employee.employees_page"))
    trung = Employee.query.filter(Employee.ma_nv == payload["ma_nv"], Employee.id != emp_id).first()
    if trung:
        flash(f"Mã nhân viên '{payload['ma_nv']}' đã được sử dụng.", "danger")
        return redirect(url_for("employee.employees_page"))

    emp.ma_nv = payload["ma_nv"]
    emp.ho_ten = payload["ho_ten"]
    emp.email = payload["email"]
    emp.bo_phan = payload["bo_phan"]
    emp.vi_tri = payload["vi_tri"]
    emp.updated_by_id = current_user.id

    db.session.commit()
    flash("Đã cập nhật thông tin nhân viên.", "success")
    return redirect(url_for("employee.employees_page"))


@bp.route("/employees/delete/<int:emp_id>", methods=["POST"])
@login_required
def employee_delete(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    db.session.delete(emp)
    db.session.commit()
    flash(f"Đã xóa nhân viên '{emp.ho_ten}'.", "success")
    return redirect(url_for("employee.employees_page"))
