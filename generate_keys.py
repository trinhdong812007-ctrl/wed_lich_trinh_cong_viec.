# -*- coding: utf-8 -*-
"""
generate_keys.py
Script sinh Key kích hoạt tài khoản
"""

import uuid

from app import create_app
from app.extensions import db
from app.models import ActivationKey


def generate_keys(count=5):
    app = create_app()
    with app.app_context():
        db.create_all()
        created_keys = []
        for _ in range(count):
            random_str = uuid.uuid4().hex[:12].upper()
            formatted_key = f"{random_str[:4]}-{random_str[4:8]}-{random_str[8:]}"

            new_key = ActivationKey(key=formatted_key)
            db.session.add(new_key)
            created_keys.append(formatted_key)

        db.session.commit()

        print(f"\n==========================================")
        print(f"✅ ĐÃ TẠO THÀNH CÔNG {count} KEY KÍCH HOẠT MỚI:")
        print(f"==========================================")
        for idx, k in enumerate(created_keys, 1):
            print(f" {idx}. {k}")
        print(f"==========================================\n")


if __name__ == "__main__":
    try:
        val = input("Nhập số lượng Key muốn sinh (Mặc định 5): ").strip()
        num = int(val) if val else 5
        generate_keys(num)
    except ValueError:
        generate_keys(5)