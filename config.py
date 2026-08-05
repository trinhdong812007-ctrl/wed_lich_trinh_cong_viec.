# -*- coding: utf-8 -*-
"""
config.py
Cấu hình hệ thống cho ứng dụng Employee Task Scheduler
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "bi-mat-khong-the-bat-mi-employee-scheduler")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
