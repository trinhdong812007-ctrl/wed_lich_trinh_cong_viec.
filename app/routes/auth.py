# -*- coding: utf-8 -*-
"""
app/routes/auth.py
Routes xác thực người dùng: đăng nhập, đăng ký, đăng xuất, sinh Key kích hoạt.
"""

import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import User, ActivationKey
from app.services.helpers import normalize_text

bp = Blueprint("auth", __name__)


@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    return redirect(url_for("dashboard.lich_trinh"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.lich_trinh"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash("Đăng nhập thành công!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.lich_trinh"))
        else:
            flash("Tài khoản hoặc mật khẩu không chính xác!", "danger")

    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.lich_trinh"))

    if request.method == "POST":
        username = normalize_text(request.form.get("username"))
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        activation_key = normalize_text(request.form.get("activation_key"))

        if not username or not password or not activation_key:
            flash("Vui lòng điền đầy đủ tất cả thông tin!", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp!", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(username=username).first():
            flash(f"Tên đăng nhập '{username}' đã được sử dụng!", "warning")
            return render_template("auth/register.html")

        key_obj = ActivationKey.query.filter_by(key=activation_key, is_used=False).first()
        if not key_obj:
            flash("Key kích hoạt không đúng hoặc đã được sử dụng!", "danger")
            return render_template("auth/register.html")

        new_user = User(username=username)
        new_user.set_password(password)
        key_obj.is_used = True

        db.session.add(new_user)
        db.session.commit()

        flash("Kích hoạt và đăng ký tài khoản thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route('/generate-keys-admin')
def generate_keys_admin():
    new_keys = []

    for _ in range(5):
        random_str = uuid.uuid4().hex[:12].upper()
        formatted_key = f"{random_str[:4]}-{random_str[4:8]}-{random_str[8:]}"

        key_obj = ActivationKey(key=formatted_key, is_used=False)
        db.session.add(key_obj)
        new_keys.append(formatted_key)

    db.session.commit()

    html_response = """
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; border: 1px solid #333; background: #1e1e2e; color: #fff; border-radius: 8px;">
        <h2 style="color: #4ef037;">✅ Đã tạo thành công 5 Key mới!</h2>
        <p>Sao chép một trong các Key dưới đây để đăng ký:</p>
        <ul style="background: #2b2b3d; padding: 15px 30px; border-radius: 5px;">
    """
    for k in new_keys:
        html_response += f"<li style='font-size: 18px; margin: 8px 0; font-weight: bold; color: #00d2ff;'>{k}</li>"
    html_response += """
        </ul>
        <br>
        <a href="/register" style="display: inline-block; padding: 10px 20px; background: #3b82f6; color: white; text-decoration: none; border-radius: 5px;">👉 Đến trang Đăng ký ngay</a>
    </div>
    """
    return html_response


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Đã đăng xuất khỏi hệ thống.", "info")
    return redirect(url_for("auth.login"))
