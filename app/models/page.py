# -*- coding: utf-8 -*-
"""
app/models/page.py
Model trang tĩnh (CMS đơn giản qua dynamic pages)
"""

from datetime import datetime

from app.extensions import db


class Page(db.Model):
    __tablename__ = "page"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    tieu_de = db.Column(db.String(200), nullable=False)
    noi_dung = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)