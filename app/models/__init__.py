# -*- coding: utf-8 -*-
"""
app/models/__init__.py
Import tất cả các model để Flask-SQLAlchemy / Alembic nhận diện đầy đủ.
"""

from app.models.user import User, ActivationKey
from app.models.employee import Employee
from app.models.task import Task
from app.models.schedule import Schedule, WeekSchedule
from app.models.tkbfile import TKBFile
from app.models.page import Page

__all__ = [
    "User",
    "ActivationKey",
    "Employee",
    "Task",
    "Schedule",
    "WeekSchedule",
    "Page",
    "TKBFile",
]