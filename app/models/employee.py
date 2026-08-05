# -*- coding: utf-8 -*-
"""
app/models/employee.py
Model nhân viên
"""

from datetime import datetime

from app.extensions import db


class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    ma_nv = db.Column(db.String(20), unique=True, nullable=False)
    ho_ten = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    bo_phan = db.Column(db.String(80))
    vi_tri = db.Column(db.String(80))
    trinh_do = db.Column(db.String(20), default="Cơ bản")  # Kept for backward compat; level now embedded in vi_tri
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    creator = db.relationship('User', foreign_keys=[created_by_id])
    updater = db.relationship('User', foreign_keys=[updated_by_id])
    schedules = db.relationship("Schedule", backref="employee", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "ma_nv": self.ma_nv,
            "ho_ten": self.ho_ten,
            "email": self.email,
            "bo_phan": self.bo_phan,
            "vi_tri": self.vi_tri,
        }
