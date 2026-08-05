# -*- coding: utf-8 -*-
"""
app/services/validation.py
Xác thực dữ liệu đầu vào cho nhân viên và công việc
"""

from app.extensions import VI_TRI_MAP, DO_UU_TIEN_LIST
from app.services.helpers import normalize_text


def validate_employee_payload(data):
    errors = []
    ma_nv = normalize_text(data.get("ma_nv"))
    ho_ten = normalize_text(data.get("ho_ten"))
    email = normalize_text(data.get("email"))
    bo_phan = normalize_text(data.get("bo_phan"))
    vi_tri = normalize_text(data.get("vi_tri"))

    if not ma_nv:
        errors.append("Mã nhân viên là bắt buộc.")
    if not ho_ten:
        errors.append("Họ tên là bắt buộc.")
    if not email:
        errors.append("Email là bắt buộc.")
    if not bo_phan:
        errors.append("Bộ phận là bắt buộc.")
    if not vi_tri:
        errors.append("Vị trí là bắt buộc.")
    if bo_phan and bo_phan not in VI_TRI_MAP:
        errors.append("Bộ phận không hợp lệ.")
    return errors


def validate_task_payload(data):
    errors = []
    ma_cv = normalize_text(data.get("ma_cv"))
    ten_cv = normalize_text(data.get("ten_cv"))
    do_uu_tien = normalize_text(data.get("do_uu_tien"))
    ngay_gio = normalize_text(data.get("ngay_gio"))
    bo_phan = normalize_text(data.get("bo_phan"))
    so_luong_nv = data.get("so_luong_nv")
    thoi_luong = data.get("thoi_luong")

    if not ma_cv:
        errors.append("Mã công việc là bắt buộc.")
    if not ten_cv:
        errors.append("Tên công việc là bắt buộc.")
    if not do_uu_tien:
        errors.append("Độ ưu tiên là bắt buộc.")
    if not bo_phan:
        errors.append("Bộ phận là bắt buộc.")
    if do_uu_tien and do_uu_tien not in DO_UU_TIEN_LIST:
        errors.append("Độ ưu tiên không hợp lệ.")

    try:
        so_luong_nv_i = int(so_luong_nv)
        if so_luong_nv_i < 1:
            errors.append("Số lượng nhân viên phải lớn hơn 0.")
    except (TypeError, ValueError):
        errors.append("Số lượng nhân viên phải là số nguyên.")

    try:
        thoi_luong_f = float(thoi_luong)
        if thoi_luong_f <= 0:
            errors.append("Thời lượng phải lớn hơn 0.")
    except (TypeError, ValueError):
        errors.append("Thời lượng phải là số.")

    return errors
