# -*- coding: utf-8 -*-
"""
app/routes/task.py
Routes quản lý công việc và phân công công việc (thủ công + AI gợi ý).
"""

from datetime import datetime, timedelta, date

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.extensions import db, DO_UU_TIEN_LIST, VI_TRI_MAP, TRINH_DO_LIST, DO_UU_TIEN_COLORS, DO_UU_TIEN_BG, THU_TRONG_TUAN
from app.models import Employee, Task, Schedule, WeekSchedule
from app.services.helpers import (
    normalize_text,
    parse_date,
    parse_date_value,
    parse_vi_tri_with_level,
    get_week_start,
    touch_last_update,
)
from app.services.validation import validate_task_payload
from app.services.scheduling import check_trung_ca, get_department_filter, assign_task_ai

bp = Blueprint("task", __name__)


@bp.route("/tasks")
@login_required
def tasks_page():
    q = request.args.get("q", "").strip()
    detail_id = request.args.get("detail", type=int)
    task_id = request.args.get("task_id", type=int)
    auto = request.args.get("auto") == "1"

    query = Task.query.filter_by(completed=False)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Task.ma_cv.ilike(like), Task.ten_cv.ilike(like), Task.ghi_chu.ilike(like)))
    tasks = query.order_by(Task.id.desc()).all()

    detail_task = None
    detail_assignments = []
    if detail_id:
        detail_task = Task.query.get(detail_id)
        if detail_task:
            detail_assignments = (
                db.session.query(Schedule, Employee)
                .join(Employee, Schedule.employee_id == Employee.id)
                .filter(Schedule.task_id == detail_id)
                .order_by(Schedule.ngay_lam_viec, Schedule.ca)
                .all()
            )

    return render_template(
        "task/tasks.html", tasks=tasks, q=q, do_uu_tien_list=DO_UU_TIEN_LIST,
        vi_tri_map=VI_TRI_MAP, trinh_do_list=TRINH_DO_LIST,
        do_uu_tien_colors=DO_UU_TIEN_COLORS, do_uu_tien_bg=DO_UU_TIEN_BG,
        detail_task=detail_task, detail_assignments=detail_assignments,
    )


@bp.route("/tasks/add", methods=["POST"])
@login_required
def task_add():
    payload = {
        "ma_cv": normalize_text(request.form.get("ma_cv")),
        "ten_cv": normalize_text(request.form.get("ten_cv")),
        "ghi_chu": normalize_text(request.form.get("ghi_chu")),
        "do_uu_tien": normalize_text(request.form.get("do_uu_tien")) or "Trung bình",
        "bo_phan": normalize_text(request.form.get("bo_phan")),
        "so_luong_nv": request.form.get("so_luong_nv", "1"),
        "thoi_luong": request.form.get("thoi_luong", "1"),
    }
    errors = validate_task_payload(payload)
    if errors:
        flash("; ".join(errors), "danger")
        return redirect(url_for("task.tasks_page"))
    if Task.query.filter_by(ma_cv=payload["ma_cv"]).first():
        flash(f"Mã công việc '{payload['ma_cv']}' đã tồn tại.", "danger")
        return redirect(url_for("task.tasks_page"))

    task = Task(
        ma_cv=payload["ma_cv"],
        ten_cv=payload["ten_cv"],
        ghi_chu=payload["ghi_chu"],
        do_uu_tien=payload["do_uu_tien"],
        ngay_gio=None,
        bo_phan=payload["bo_phan"],
        so_luong_nv=int(payload["so_luong_nv"]),
        thoi_luong=float(payload["thoi_luong"]),
        ca_requirement=None,
        created_by_id=current_user.id,
        updated_by_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    touch_last_update()
    flash(f"Đã thêm công việc '{payload['ten_cv']}' thành công.", "success")
    return redirect(url_for("task.tasks_page"))


@bp.route("/tasks/edit/<int:task_id>", methods=["POST"])
@login_required
def task_edit(task_id):
    task = Task.query.get_or_404(task_id)
    payload = {
        "ma_cv": normalize_text(request.form.get("ma_cv")),
        "ten_cv": normalize_text(request.form.get("ten_cv")),
        "ghi_chu": normalize_text(request.form.get("ghi_chu")),
        "do_uu_tien": normalize_text(request.form.get("do_uu_tien")) or "Trung bình",
        "bo_phan": normalize_text(request.form.get("bo_phan")),
        "so_luong_nv": request.form.get("so_luong_nv", "1"),
        "thoi_luong": request.form.get("thoi_luong", "1"),
    }
    errors = validate_task_payload(payload)
    if errors:
        flash("; ".join(errors), "danger")
        return redirect(url_for("task.tasks_page"))
    trung = Task.query.filter(Task.ma_cv == payload["ma_cv"], Task.id != task_id).first()
    if trung:
        flash(f"Mã công việc '{payload['ma_cv']}' đã được sử dụng.", "danger")
        return redirect(url_for("task.tasks_page"))
    task.ma_cv = payload["ma_cv"]
    task.ten_cv = payload["ten_cv"]
    task.ghi_chu = payload["ghi_chu"]
    task.do_uu_tien = payload["do_uu_tien"]
    task.bo_phan = payload["bo_phan"]
    task.so_luong_nv = int(payload["so_luong_nv"])
    task.thoi_luong = float(payload["thoi_luong"])
    task.updated_at = datetime.utcnow()
    task.updated_by_id = current_user.id

    db.session.commit()
    touch_last_update()
    flash("Đã cập nhật công việc.", "success")
    return redirect(url_for("task.tasks_page"))


@bp.route("/tasks/delete/<int:task_id>", methods=["POST"])
@login_required
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    Schedule.query.filter_by(task_id=task.id).delete()
    WeekSchedule.query.filter_by(task_id=task.id).delete()
    db.session.delete(task)
    db.session.commit()
    touch_last_update()
    flash(f"Đã xóa công việc '{task.ten_cv}'.", "success")
    return redirect(url_for("task.tasks_page"))


@bp.route("/tasks/complete/<int:task_id>", methods=["POST"])
@login_required
def task_complete(task_id):
    task = Task.query.get_or_404(task_id)
    Schedule.query.filter(Schedule.task_id == task.id).update({"week_schedule_id": None})
    WeekSchedule.query.filter_by(task_id=task.id).delete()
    task.completed = True
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()
    task.updated_by_id = current_user.id
    db.session.commit()
    touch_last_update()
    flash(f"Đã đánh dấu công việc '{task.ten_cv}' hoàn thành.", "success")
    return redirect(url_for("task.tasks_page"))


@bp.route("/tasks/history")
@login_required
def task_history():
    q = request.args.get("q", "").strip()
    detail_id = request.args.get("detail", type=int)
    query = Task.query.filter_by(completed=True)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Task.ma_cv.ilike(like), Task.ten_cv.ilike(like), Task.ghi_chu.ilike(like)))
    tasks = query.order_by(Task.completed_at.desc()).all()
    detail_task = None
    detail_assignments = []
    if detail_id:
        detail_task = Task.query.get(detail_id)
        if detail_task:
            detail_assignments = (
                db.session.query(Schedule, Employee)
                .join(Employee, Schedule.employee_id == Employee.id)
                .filter(Schedule.task_id == detail_id)
                .order_by(Schedule.ngay_lam_viec, Schedule.ca)
                .all()
            )
    return render_template(
        "task/task_history.html", tasks=tasks, q=q, do_uu_tien_list=DO_UU_TIEN_LIST,
        vi_tri_map=VI_TRI_MAP, trinh_do_list=TRINH_DO_LIST,
        do_uu_tien_colors=DO_UU_TIEN_COLORS, do_uu_tien_bg=DO_UU_TIEN_BG,
        detail_task=detail_task, detail_assignments=detail_assignments
    )


@bp.route("/tasks/assign")
@login_required
def task_assign():
    tasks = Task.query.filter_by(completed=False).order_by(Task.id.desc()).all()
    week_start = get_week_start(date.today())
    week_dates = [week_start + timedelta(days=i) for i in range(7)]
    week_schedule = WeekSchedule.query.filter(
        WeekSchedule.ngay_lam_viec >= week_start,
        WeekSchedule.ngay_lam_viec <= week_dates[-1]
    ).order_by(WeekSchedule.ngay_lam_viec, WeekSchedule.ca, WeekSchedule.vi_tri).all()
    recent = (
        db.session.query(Schedule, Employee, Task)
        .join(Employee, Schedule.employee_id == Employee.id)
        .join(Task, Schedule.task_id == Task.id)
        .order_by(Schedule.id.desc())
        .limit(20)
        .all()
    )
    assign_mode = "auto" if request.args.get("auto") == "1" else "manual"
    return render_template(
        "task/task_assign.html",
        tasks=tasks,
        week_schedule=week_schedule,
        week_start=week_start,
        week_dates=week_dates,
        thu_list=THU_TRONG_TUAN,
        recent=recent,
        assign_mode=assign_mode,
        today_str=date.today().strftime("%Y-%m-%d"),
        do_uu_tien_colors=DO_UU_TIEN_COLORS,
        do_uu_tien_bg=DO_UU_TIEN_BG,
        trinh_do_list=TRINH_DO_LIST,
        vi_tri_map=VI_TRI_MAP,
    )


@bp.route("/tasks/assign/delete/<int:schedule_id>", methods=["POST"])
@login_required
def delete_assignment_route(schedule_id):
    sch = Schedule.query.get_or_404(schedule_id)
    task_id = sch.task_id

    try:
        db.session.delete(sch)
        db.session.commit()
        flash("Đã xóa phân công nhân viên thành công!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Có lỗi xảy ra khi xóa!", "danger")

    return redirect(request.referrer or url_for('task.tasks_page', detail=task_id))


@bp.route("/tasks/assign/get-employees", methods=["POST"])
@login_required
def assign_get_employees():
    data = request.get_json()
    task_id = data.get("task_id")
    ngay_str = data.get("ngay_lam_viec")
    ca = data.get("ca", "Sáng")

    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Công việc không tồn tại"}), 404

    ngay = parse_date_value(ngay_str) if ngay_str else None

    query = Employee.query
    departments = get_department_filter(task)
    if departments:
        query = query.filter(Employee.bo_phan.in_(departments))

    employees = query.all()

    result = []
    for emp in employees:
        available = True
        msg = ""
        if ngay:
            existing = check_trung_ca(emp.id, ngay, ca)
            if existing:
                available = False
                msg = f"Đã có lịch '{existing.task.ten_cv}' ca {ca}"
        result.append({
            "id": emp.id,
            "ma_nv": emp.ma_nv,
            "ho_ten": emp.ho_ten,
            "email": emp.email,
            "bo_phan": emp.bo_phan,
            "vi_tri": emp.vi_tri,
            "available": available,
            "msg": msg,
        })

    assigned_count = Schedule.query.filter_by(task_id=task.id).count()

    return jsonify({
        "employees": result,
        "max_nv": task.so_luong_nv,
        "assigned_count": assigned_count,
        "remaining_slots": max(0, task.so_luong_nv - assigned_count),
        "ca": ca
    })


@bp.route("/tasks/assign/ai-suggest", methods=["POST"])
@login_required
def assign_ai_suggest():
    data = request.get_json()
    task_id = data.get("task_id")
    ngay_str = data.get("ngay_lam_viec")
    ca = data.get("ca", "Sáng")

    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Công việc không tồn tại"}), 404

    ngay = parse_date_value(ngay_str) if ngay_str else None

    query = Employee.query
    departments = get_department_filter(task)
    if departments:
        query = query.filter(Employee.bo_phan.in_(departments))
    employees = query.all()

    scored = []
    for emp in employees:
        score = 0
        _, trinh_do = parse_vi_tri_with_level(emp.vi_tri or "")
        if trinh_do == "Chuyên gia":
            score += 40
        elif trinh_do == "Thành thạo":
            score += 30
        elif trinh_do == "Khá":
            score += 20
        elif trinh_do == "Cơ bản":
            score += 10

        available = True
        if ngay:
            existing = check_trung_ca(emp.id, ngay, ca)
            if existing:
                available = False
                score -= 100

        total_assigned = Schedule.query.filter_by(employee_id=emp.id).count()
        score -= total_assigned * 2

        scored.append({
            "id": emp.id,
            "ma_nv": emp.ma_nv,
            "ho_ten": emp.ho_ten,
            "bo_phan": emp.bo_phan,
            "vi_tri": emp.vi_tri,
            "score": max(score, 0) if available else 0,
            "available": available,
            "recommended": available and score > 20,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(scored[:task.so_luong_nv * 3])


@bp.route("/tasks/assign/save", methods=["POST"])
@login_required
def assign_save():
    data = request.get_json()
    task_id = data.get("task_id")
    employee_ids = data.get("employee_ids", [])
    week_schedule_id = data.get("week_schedule_id")

    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Công việc không tồn tại."}), 404

    ws_entry = None
    if week_schedule_id:
        ws_entry = WeekSchedule.query.get(week_schedule_id)

    if not ws_entry:
        ngay_str = data.get("ngay_lam_viec")
        ca = data.get("ca", "Sáng")
        if not ngay_str:
            return jsonify({"error": "Thiếu ngày làm việc."}), 400
        ngay = parse_date_value(ngay_str)
        if not ngay:
            return jsonify({"error": "Ngày làm việc không hợp lệ."}), 400
    else:
        ngay = ws_entry.ngay_lam_viec
        ca = ws_entry.ca

    current_assigned_count = Schedule.query.filter_by(task_id=task.id).count()
    total_after_assign = current_assigned_count + len(employee_ids)

    if total_after_assign > task.so_luong_nv:
        return jsonify({
            "error": f"Vượt quá số lượng quy định! Công việc này cần tối đa {task.so_luong_nv} nhân viên (hiện tại đã phân công {current_assigned_count})."
        }), 400

    assigned = []
    errors = []

    for eid in employee_ids:
        already_in_task = Schedule.query.filter_by(employee_id=eid, task_id=task_id, ngay_lam_viec=ngay, ca=ca).first()
        if already_in_task:
            emp = Employee.query.get(eid)
            errors.append(f"Nhân viên '{emp.ho_ten}' đã được phân công ca này.")
            continue

        trung = check_trung_ca(eid, ngay, ca)
        if trung:
            emp = Employee.query.get(eid)
            errors.append(f"Nhân viên '{emp.ho_ten}' đã có lịch trùng ở ca {ca}.")
            continue

        sch = Schedule(
            employee_id=eid,
            task_id=task_id,
            ngay_lam_viec=ngay,
            ca=ca,
            week_schedule_id=week_schedule_id,
            created_by_id=current_user.id,
            updated_by_id=current_user.id
        )
        db.session.add(sch)
        assigned.append(eid)

    db.session.commit()
    touch_last_update()
    return jsonify({"assigned": len(assigned), "errors": errors})


@bp.route("/tasks/assign/auto-all", methods=["POST"])
@login_required
def auto_assign_all_tasks():
    week_start = get_week_start(date.today())
    ws_entries = WeekSchedule.query.filter(
        WeekSchedule.ngay_lam_viec >= week_start,
        WeekSchedule.ngay_lam_viec < week_start + timedelta(days=7)
    ).all()

    total_assigned = 0
    total_errors = []

    for ws_entry in ws_entries:
        if ws_entry.task.completed:
            continue
        assigned, errors = assign_task_ai(ws_entry, user_id=current_user.id)
        total_assigned += len(assigned)
        total_errors.extend(errors)

    db.session.commit()
    touch_last_update()
    if total_assigned:
        flash(f"AI đã tự động phân công {total_assigned} ca.", "success")
    else:
        msg = "AI không thể phân công thêm ca nào."
        if total_errors:
            msg += " Lỗi: " + "; ".join(total_errors[:5])
        flash(msg, "warning")
    return redirect(url_for("task.tasks_page"))


@bp.route("/api/check_conflict")
@login_required
def api_check_conflict():
    employee_id = request.args.get("employee_id", type=int)
    ngay_str = request.args.get("ngay_lam_viec")
    ca = request.args.get("ca")

    if not employee_id or not ngay_str or not ca:
        return jsonify({"conflict": False})
    ngay = parse_date(ngay_str)
    trung = check_trung_ca(employee_id, ngay, ca)
    if trung:
        return jsonify({"conflict": True, "task_name": trung.task.ten_cv})
    return jsonify({"conflict": False})
