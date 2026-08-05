# -*- coding: utf-8 -*-
"""
app/models/tkbfile.py
Model lưu trữ file Thời khóa biểu tuần (TKB_tuan) đang được áp dụng.
"""

from datetime import datetime

from app.extensions import db


class TKBFile(db.Model):
    __tablename__ = "tkb_file"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.LargeBinary, nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    creator = db.relationship('User', foreign_keys=[created_by_id])