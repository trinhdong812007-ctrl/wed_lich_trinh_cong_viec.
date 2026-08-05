# -*- coding: utf-8 -*-
"""
app/routes/__init__.py
Đăng ký tất cả Blueprints cho ứng dụng.
"""


def register_blueprints(app):
    from app.routes.auth import bp as auth_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.employee import bp as employee_bp
    from app.routes.task import bp as task_bp
    from app.routes.schedule import bp as schedule_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(schedule_bp)
