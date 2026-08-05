# -*- coding: utf-8 -*-
"""
app/routes/dashboard.py
Routes Dashboard: lịch làm việc tuần, báo cáo thống kê, các API trạng thái.
"""

import os
from datetime import datetime, timedelta, date

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from config import BASE_DIR
from app.extensions import db, THU_TRONG_TUAN, DO_UU_TIEN_COLORS, DO_UU_TIEN_BG
from app.models import Employee, Task, Schedule, WeekSchedule
from app.services.helpers import parse_date, get_week_start, touch_last_update

bp = Blueprint("dashboard", __name__)


@bp.route("/lich-trinh")
@login_required
def lich_trinh():
    start_param = request.args.get("start")
    if start_param:
        anchor = parse_date(start_param)
    else:
        anchor = date.today()
    week_start = get_week_start(anchor)
    week_dates = [week_start + timedelta(days=i) for i in range(7)]

    schedule_entries = db.session.query(Schedule, Employee, Task).join(
        Employee, Schedule.employee_id == Employee.id
    ).join(
        Task, Schedule.task_id == Task.id
    ).filter(
        Schedule.ngay_lam_viec >= week_dates[0],
        Schedule.ngay_lam_viec <= week_dates[-1],
        Task.completed == False
    ).order_by(Schedule.ngay_lam_viec, Schedule.ca).all()

    week_schedule_entries = WeekSchedule.query.filter(
        WeekSchedule.ngay_lam_viec >= week_dates[0],
        WeekSchedule.ngay_lam_viec <= week_dates[-1]
    ).order_by(WeekSchedule.ngay_lam_viec, WeekSchedule.ca, WeekSchedule.vi_tri).all()

    timetable = {}
    week_tasks = set()

    for ws in week_schedule_entries:
        key = (ws.ngay_lam_viec, ws.ca)
        task = ws.task
        if task.completed:
            continue
        if key not in timetable:
            timetable[key] = []
        timetable[key].append({
            "task": task,
            "employees": [],
            "week_schedule_id": ws.id,
            "vi_tri": ws.vi_tri,
        })
        week_tasks.add(task.id)

    for sch, emp, task in schedule_entries:
        key = (sch.ngay_lam_viec, sch.ca)
        if key not in timetable:
            timetable[key] = []
        found = False
        for entry in timetable[key]:
            if entry["task"].id == task.id:
                entry["employees"].append(emp)
                found = True
                break
        if not found:
            timetable[key].append({
                "task": task,
                "employees": [emp],
                "week_schedule_id": None,
                "vi_tri": 0,
            })
        week_tasks.add(task.id)

    week_tasks_dict = {}
    for sch, emp, task in schedule_entries:
        key = (task.id, sch.ngay_lam_viec, sch.ca)
        if key not in week_tasks_dict:
            week_tasks_dict[key] = {
                "task": task,
                "date": sch.ngay_lam_viec,
                "ca": sch.ca,
                "employees": [],
            }
        week_tasks_dict[key]["employees"].append(emp)
    week_tasks_list = list(week_tasks_dict.values())

    prev_week = week_start - timedelta(days=7)
    next_week = week_start + timedelta(days=7)
    total_employees = Employee.query.count()

    return render_template(
        "dashboard/lich_trinh.html",
        week_start=week_start,
        week_dates=week_dates,
        thu_list=THU_TRONG_TUAN,
        timetable=timetable,
        week_tasks=week_tasks_list,
        prev_week=prev_week.strftime("%Y-%m-%d"),
        next_week=next_week.strftime("%Y-%m-%d"),
        today_str=date.today().strftime("%Y-%m-%d"),
        total_employees=total_employees,
        do_uu_tien_colors=DO_UU_TIEN_COLORS,
        do_uu_tien_bg=DO_UU_TIEN_BG,
    )


@bp.route("/reports")
@login_required
def reports_page():
    employees = Employee.query.order_by(Employee.ho_ten).all()
    stats = []
    for emp in employees:
        count = Schedule.query.filter_by(employee_id=emp.id).count()
        total_hours = (
            db.session.query(db.func.sum(Task.thoi_luong))
            .join(Schedule, Schedule.task_id == Task.id)
            .filter(Schedule.employee_id == emp.id)
            .scalar() or 0
        )
        stats.append({"employee": emp, "so_luong_ca": count, "tong_gio": round(total_hours, 1)})
    stats.sort(key=lambda x: x["so_luong_ca"], reverse=True)
    tong_lich = Schedule.query.count()
    tong_nv_co_lich = db.session.query(Schedule.employee_id).distinct().count()
    bo_phan_stats = {}
    for emp in employees:
        bp_name = emp.bo_phan or "Chưa phân loại"
        bo_phan_stats[bp_name] = bo_phan_stats.get(bp_name, 0) + Schedule.query.filter_by(employee_id=emp.id).count()
    return render_template(
        "dashboard/reports.html",
        stats=stats,
        tong_lich=tong_lich,
        tong_nv_co_lich=tong_nv_co_lich,
        bo_phan_stats=bo_phan_stats
    )


@bp.route('/api/last-update')
def api_last_update():
    update_file = os.path.join(BASE_DIR, ".last_update")
    if not os.path.exists(update_file):
        touch_last_update()
    mtime = datetime.utcfromtimestamp(os.path.getmtime(update_file))
    return jsonify({"last_update": mtime.isoformat()})


@bp.route("/api/check-ai-readiness")
@login_required
def api_check_ai_readiness():
    emp_count = Employee.query.count()
    task_count = Task.query.filter_by(completed=False).count()
    week_start = get_week_start(date.today())
    ws_count = WeekSchedule.query.filter(
        WeekSchedule.ngay_lam_viec >= week_start,
        WeekSchedule.ngay_lam_viec < week_start + timedelta(days=7)
    ).count()

    missing = []
    if emp_count == 0:
        missing.append("Nhân viên")
    if task_count == 0:
        missing.append("Công việc")
    if ws_count == 0:
        missing.append("Thời khóa biểu tuần (TKB_tuan)")

    ready = len(missing) == 0
    return jsonify({
        "ready": ready,
        "missing": missing,
        "employees": emp_count,
        "tasks": task_count,
        "week_schedule": ws_count,
    })
