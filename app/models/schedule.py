# -*- coding: utf-8 -*-
"""
app/models/schedule.py
Model phân công lịch làm việc (Schedule) và lịch tuần (WeekSchedule)
"""

from datetime import datetime

from app.extensions import db


class WeekSchedule(db.Model):
    __tablename__ = "week_schedule"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    ngay_lam_viec = db.Column(db.Date, nullable=False)
    ca = db.Column(db.String(10), nullable=False)
    vi_tri = db.Column(db.Integer, default=1)
    week_start = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    task = db.relationship("Task", backref="week_schedules")
    creator = db.relationship('User', foreign_keys=[created_by_id])
    updater = db.relationship('User', foreign_keys=[updated_by_id])

    __table_args__ = (db.UniqueConstraint("task_id", "ngay_lam_viec", "ca", name="uq_week_schedule"),)


class Schedule(db.Model):
    __tablename__ = "schedule"
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    ngay_lam_viec = db.Column(db.Date, nullable=False)
    ca = db.Column(db.String(10), nullable=False)
    week_schedule_id = db.Column(db.Integer, db.ForeignKey("week_schedule.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    week_schedule_rel = db.relationship("WeekSchedule", backref="schedules")
    creator = db.relationship('User', foreign_keys=[created_by_id])
    updater = db.relationship('User', foreign_keys=[updated_by_id])
    __table_args__ = (db.UniqueConstraint("employee_id", "ngay_lam_viec", "ca", name="uq_emp_day_ca"),)
