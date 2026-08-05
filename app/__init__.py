# -*- coding: utf-8 -*-
"""
app/__init__.py
Khởi tạo ứng dụng Flask (Application Factory), đăng ký Blueprints
và thực hiện các bước khởi tạo cơ sở dữ liệu.
"""

import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    from app.routes import register_blueprints
    register_blueprints(app)

    from app.models import User
    from app.services.schema import init_db, seed_admin

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        init_db()
        seed_admin()

    return app
