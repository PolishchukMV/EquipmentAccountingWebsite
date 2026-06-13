#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для сброса паролей тестовых пользователей.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from apps.accounts.models import CustomUser

# Пароли для всех пользователей
users_data = [
    ('admin', 'admin123', 'Администратор'),
    ('manager', 'manager123', 'Менеджер'),
    ('employee', 'employee123', 'Сотрудник'),
    ('auditor', 'auditor123', 'Аудитор'),
]

print("Сброс паролей тестовых пользователей...\n")

for username, password, role_name in users_data:
    try:
        user = CustomUser.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"[OK] Пароль пользователя '{username}' ({role_name}) обновлён")
    except CustomUser.DoesNotExist:
        print(f"[WARN] Пользователь '{username}' не найден")
    except Exception as e:
        print(f"[ERROR] Ошибка при обновлении '{username}': {e}")

print("\nГотово! Теперь можно войти с новыми паролями.")
