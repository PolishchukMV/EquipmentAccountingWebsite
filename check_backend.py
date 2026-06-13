#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Проверка ModelBackend.
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
    print(f"  is_active: {user.is_active}")
    print(f"  can_authenticate: {user.can_authenticate()}")
    
    # get_user
    retrieved = backend.get_user(user.pk)
    print(f"  get_user(pk): {retrieved}")
    
    # Проверяем permissions
    from django.contrib.auth.models import Permission
    perms = user.get_all_permissions()
    print(f"  permissions: {len(perms)} прав")
