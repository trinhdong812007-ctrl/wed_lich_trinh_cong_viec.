# -*- coding: utf-8 -*-
"""
app/services/scheduling.py
Business logic về phân công công việc và kiểm tra trùng ca
"""

from app.extensions import db
from app.models.employee import Employee
from app.models.task import Task
from app.models.schedule import Schedule
from app.services.helpers import parse_vi_tri_with_level


def check_trung_ca(employee_id, ngay_lam_viec, ca, exclude_id=None):
    query = Schedule.query.filter_by(employee_id=employee_id, ngay_lam_viec=ngay_lam_viec, ca=ca)
    if exclude_id:
        query = query.filter(Schedule.id != exclude_id)
    return query.first()


def get_department_filter(task):
    if not task.bo_phan:
        return []
    departments = [d.strip() for d in task.bo_phan.split(",")]
    return [d for d in departments if d]


def get_ai_suggested_employee_ids(task, ngay_lam_viec, ca="Sáng", limit=None):
    if not task:
        return []
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
        if ngay_lam_viec:
            existing = check_trung_ca(emp.id, ngay_lam_viec, ca)
            if existing:
                available = False
                score -= 100

        total_assigned = Schedule.query.filter_by(employee_id=emp.id).count()
        score -= total_assigned * 2

        scored.append({"id": emp.id, "score": score, "available": available})

    scored.sort(key=lambda x: x["score"], reverse=True)
    suggested = [item["id"] for item in scored if item["available"]]

    return suggested


def assign_task_ai(ws_entry, user_id=None):
    if not ws_entry:
        return [], ["Không tìm thấy lịch tuần."]
    task = ws_entry.task
    ca = ws_entry.ca
    ngay = ws_entry.ngay_lam_viec
    suggested_ids = get_ai_suggested_employee_ids(task, ngay, ca=ca)
    if not suggested_ids:
        return [], ["Không tìm thấy nhân viên phù hợp."]

    max_nv = task.so_luong_nv or 1
    already_assigned = Schedule.query.filter_by(task_id=task.id).count()
    remaining = max(0, max_nv - already_assigned)
    if remaining <= 0:
        return [], [f"Công việc '{task.ten_cv}' đã đủ tối đa {task.so_luong_nv} nhân viên."]

    assigned = []
    errors = []
    for eid in suggested_ids:
        if len(assigned) >= remaining:
            break
        if check_trung_ca(eid, ngay, ca):
            emp = Employee.query.get(eid)
            errors.append(f"Nhân viên '{emp.ho_ten}' đã có lịch ca {ca}.")
            continue
        db.session.add(Schedule(
            employee_id=eid,
            task_id=task.id,
            ngay_lam_viec=ngay,
            ca=ca,
            week_schedule_id=ws_entry.id,
            created_by_id=user_id,
            updated_by_id=user_id
        ))
        assigned.append(eid)
    return assigned, errors
