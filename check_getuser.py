#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Проверка get_user с деталями.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()
backend = ModelBackend()

print(f"User model: {User}")
print(f"User._meta.db_table: {User._meta.db_table}")

for pk in [1, 33]:
    print(f"\nPK: {pk}")
    
    # Прямой запрос
    try:
        direct = User.objects.get(pk=pk)
        print(f"  User.objects.get(pk={pk}): {direct.username}")
    except Exception as e:
        print(f"  User.objects.get(pk={pk}): ERROR - {e}")
    
    # Через backend
    try:
        backend_user = backend.get_user(pk)
        print(f"  backend.get_user({pk}): {backend_user.username if backend_user else None}")
    except Exception as e:
        print(f"  backend.get_user({pk}): ERROR - {e}")
