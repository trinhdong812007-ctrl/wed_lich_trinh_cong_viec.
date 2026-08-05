# -*- coding: utf-8 -*-
"""
extensions.py
Các đối tượng dùng chung cho toàn ứng dụng:
- db: SQLAlchemy instance
- login_manager: Flask-Login manager
- Các hằng số nghiệp vụ (ca làm việc, độ ưu tiên, bộ phận, màu sắc...)
"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Vui lòng đăng nhập để sử dụng hệ thống."
login_manager.login_message_category = "warning"

CA_LAM_VIEC = {"Sáng": "07:30 - 11:30", "Chiều": "13:00 - 17:00"}
THU_TRONG_TUAN = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
DO_UU_TIEN_LIST = ["Thấp", "Trung bình", "Cao", "Khẩn cấp"]
TRINH_DO_LIST = ["Cơ bản", "Khá", "Thành thạo", "Chuyên gia"]

VI_TRI_MAP = {
    "Kỹ thuật": ["Kỹ sư", "Kỹ thuật viên", "Trưởng phòng Kỹ thuật", "Phó phòng Kỹ thuật"],
    "Kinh doanh": ["Nhân viên Kinh doanh", "Trưởng phòng Kinh doanh", "Chuyên viên Kinh doanh"],
    "Kế toán": ["Kế toán viên", "Kế toán trưởng", "Kế toán tổng hợp"],
    "Hành chính": ["Nhân viên Hành chính", "Trưởng phòng Hành chính", "Thư ký"],
    "IT Support": ["Nhân viên IT", "Trưởng nhóm IT", "Chuyên viên IT"],
    "Nhân sự": ["Nhân viên Nhân sự", "Trưởng phòng Nhân sự", "Chuyên viên Nhân sự"],
    "Marketing": ["Nhân viên Marketing", "Trưởng phòng Marketing", "Chuyên viên Marketing"],
}

DO_UU_TIEN_COLORS = {
    "Khẩn cấp": "#fca5a5",
    "Cao": "#fcd34d",
    "Trung bình": "#93c5fd",
    "Thấp": "#cbd5e1",
}

DO_UU_TIEN_BG = {
    "Khẩn cấp": "rgba(239,68,68,0.35)",
    "Cao": "rgba(245,158,11,0.35)",
    "Trung bình": "rgba(59,130,246,0.30)",
    "Thấp": "rgba(148,163,184,0.25)",
}

TRINH_DO_ORDER = {"Cơ bản": 1, "Khá": 2, "Thành thạo": 3, "Chuyên gia": 4}
