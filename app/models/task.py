# -*- coding: utf-8 -*-
"""
app/models/task.py
Model công việc
"""

from datetime import datetime

from app.extensions import db


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    ma_cv = db.Column(db.String(20), unique=True, nullable=False)
    ten_cv = db.Column(db.String(150), nullable=False)
    ghi_chu = db.Column(db.Text)
    do_uu_tien = db.Column(db.String(20), default="Trung bình")
    ngay_gio = db.Column(db.DateTime)
    bo_phan = db.Column(db.String(80))
    so_luong_nv = db.Column(db.Integer, default=1)
    thoi_luong = db.Column(db.Float, default=1.0)
    ca_requirement = db.Column(db.String(20), default="Sáng")
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    creator = db.relationship('User', foreign_keys=[created_by_id])
    updater = db.relationship('User', foreign_keys=[updated_by_id])
    schedules = db.relationship("Schedule", backref="task", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ma_cv": self.ma_cv,
            "ten_cv": self.ten_cv,
            "ghi_chu": self.ghi_chu,
            "do_uu_tien": self.do_uu_tien,
            "bo_phan": self.bo_phan,
            "so_luong_nv": self.so_luong_nv,
            "thoi_luong": self.thoi_luong,
        }
