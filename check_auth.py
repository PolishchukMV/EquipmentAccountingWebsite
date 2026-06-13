#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Диагностика проблем с аутентификацией.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.contrib.auth import authenticate
from apps.accounts.models import CustomUser

print("=== Диагностика пользователей ===\n")

users = ['admin', 'manager', 'employee', 'auditor']

for username in users:
    try:
        user = CustomUser.objects.get(username=username)
        print(f"\nПользователь: {username}")
        print(f"  - is_active: {user.is_active}")
        print(f"  - is_staff: {user.is_staff}")
        print(f"  - is_superuser: {user.is_superuser}")
        print(f"  - role: {user.role}")
        print(f"  - has_usable_password: {user.has_usable_password()}")
        
        # Пробуем аутентифицировать
        auth = authenticate(username=username, password=f'{username}123')
        if auth:
            print(f"  - authenticate(): OK")
        else:
            print(f"  - authenticate(): FAILED (возвращает None)")
            
    except CustomUser.DoesNotExist:
        print(f"\nПользователь '{username}' НЕ НАЙДЕН")

print("\n\n=== Проверка AUTHENTICATION_BACKENDS ===")
from django.conf import settings
print(f"BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
