#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Детальная диагностика аутентификации.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from apps.accounts.models import CustomUser

print("=== Детальная диагностика ===\n")

for username in ['manager', 'employee']:
    user = CustomUser.objects.get(username=username)
    password = f'{username}123'
    
    print(f"\nПользователь: {username}")
    print(f"  password: {password}")
    print(f"  password_hash: {user.password[:20]}...")
    print(f"  check_password: {user.check_password(password)}")
    
    # Пробуем ModelBackend напрямую
    backend = ModelBackend()
    user_auth = backend.authenticate(None, username=username, password=password)
    print(f"  ModelBackend.authenticate: {user_auth}")
    
    # Пробуем без backend
    auth = authenticate(username=username, password=password)
    print(f"  authenticate(): {auth}")
    
    # Проверка поля username
    print(f"  user.username: {user.username}")
    print(f"  USERNAME_FIELD: {CustomUser.USERNAME_FIELD}")
