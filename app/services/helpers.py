# -*- coding: utf-8 -*-
"""
app/services/helpers.py
Các hàm tiện ích dùng chung: parse ngày tháng, chuẩn hóa văn bản, tính tuần...
"""

import os
from datetime import datetime, timedelta, date

from config import BASE_DIR
from app.extensions import TRINH_DO_LIST


def normalize_text(value):
    return str(value).strip() if value is not None else ""


def parse_date(value, default=None):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return default or date.today()


def parse_date_value(value):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.strptime(str(value), "%d/%m/%Y").date()
        except ValueError:
            return None


def get_week_start(d):
    return d - timedelta(days=d.weekday())


def parse_vi_tri_with_level(vi_tri_str):
    import re
    match = re.match(r'^(.+)\(([^)]+)\)$', vi_tri_str)
    if match:
        position = match.group(1).strip()
        level = match.group(2).strip()
        if level in TRINH_DO_LIST:
            return position, level
    return vi_tri_str, "Cơ bản"


def touch_last_update():
    update_file = os.path.join(BASE_DIR, ".last_update")
    with open(update_file, "w", encoding="utf-8") as f:
        f.write(datetime.utcnow().isoformat())
    os.utime(update_file, None)
    return update_file
