#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Проверка методов ModelBackend.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.contrib.auth.backends import ModelBackend
from apps.accounts.models import CustomUser

backend = ModelBackend()

for username in ['admin', 'manager']:
    user = CustomUser.objects.get(username=username)
    
    print(f"\nПользователь: {username}")
    
    # get_user
    retrieved = backend.get_user(user.pk)
    print(f"  get_user(pk={user.pk}): {retrieved}")
    print(f"  retrieved is user: {retrieved is user}")
    
    # get_by_natural_key
    by_key = CustomUser.objects.get_by_natural_key(username)
    print(f"  get_by_natural_key: {by_key}")
    
    # Проверка ModelBackend._get_user
    try:
        user_from_backend = backend._get_user(username)
        print(f"  _get_user(username): {user_from_backend}")
    except Exception as e:
        print(f"  _get_user(username): ERROR - {e}")
    
    # Проверка is_active через can_authenticate
    print(f"  can_authenticate(): {user.can_authenticate()}")
