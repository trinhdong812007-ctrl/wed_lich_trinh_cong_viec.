# -*- coding: utf-8 -*-
"""
app/services/schema.py
Khởi tạo cơ sở dữ liệu: tạo bảng, nâng cấp schema cho DB cũ, tạo tài khoản admin mặc định.
"""

import os

from sqlalchemy import text

from config import BASE_DIR
from app.extensions import db
from app.models import User


def ensure_task_schema():
    db_path = os.path.join(BASE_DIR, "instance", "database.db")
    if not os.path.exists(db_path):
        return

    with db.engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(task)"))
        columns = [row[1] for row in result]
        if "ca_requirement" not in columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN ca_requirement VARCHAR(20) DEFAULT 'Sáng'"))
        if "updated_at" not in columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN updated_at DATETIME"))
            conn.execute(text("UPDATE task SET updated_at = created_at WHERE updated_at IS NULL"))
        if "created_by_id" not in columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN created_by_id INTEGER REFERENCES users(id)"))
        if "updated_by_id" not in columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN updated_by_id INTEGER REFERENCES users(id)"))

        result = conn.execute(text("PRAGMA table_info(employee)"))
        emp_columns = [row[1] for row in result]
        if "created_by_id" not in emp_columns:
            conn.execute(text("ALTER TABLE employee ADD COLUMN created_by_id INTEGER REFERENCES users(id)"))
        if "updated_by_id" not in emp_columns:
            conn.execute(text("ALTER TABLE employee ADD COLUMN updated_by_id INTEGER REFERENCES users(id)"))

        result = conn.execute(text("PRAGMA table_info(schedule)"))
        schedule_columns = [row[1] for row in result]
        if "updated_at" not in schedule_columns:
            conn.execute(text("ALTER TABLE schedule ADD COLUMN updated_at DATETIME"))
            conn.execute(text("UPDATE schedule SET updated_at = created_at WHERE updated_at IS NULL"))
        if "created_by_id" not in schedule_columns:
            conn.execute(text("ALTER TABLE schedule ADD COLUMN created_by_id INTEGER REFERENCES users(id)"))
        if "updated_by_id" not in schedule_columns:
            conn.execute(text("ALTER TABLE schedule ADD COLUMN updated_by_id INTEGER REFERENCES users(id)"))
        if "week_schedule_id" not in schedule_columns:
            conn.execute(text("ALTER TABLE schedule ADD COLUMN week_schedule_id INTEGER REFERENCES week_schedule(id)"))

        conn.execute(text("UPDATE task SET ca_requirement=NULL WHERE ca_requirement IS NOT NULL"))


def init_db():
    ensure_task_schema()
    db.create_all()


def seed_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin_user = User(username="admin")
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.commit()
        print("Đã tự động tạo tài khoản: admin / admin123")
