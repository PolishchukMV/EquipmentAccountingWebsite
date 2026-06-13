#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Отладка views и URL.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.test import Client, RequestFactory
from django.urls import reverse

client = Client()

print("\n=== Проверка URL маршрутов ===")
urls_to_check = [
    ('equipment:equipment_list', []),
    ('equipment:category_list', []),
    ('equipment:equipment_detail', [1]),
    ('equipment:equipment_create', []),
    ('departments:department_list', []),
    ('accounts:login', []),
    ('accounts:register', []),
]

from django.urls import reverse, NoReverseMatch

for url_name, args in urls_to_check:
    try:
        url = reverse(url_name, args=args)
        print(f"[OK] {url_name} -> {url}")
    except NoReverseMatch as e:
        print(f"[FAIL] {url_name} -> {e}")

print("\n=== Проверка страниц ===")
test_urls = [
    '/',
    '/equipment/',
    '/equipment/categories/',
    '/departments/',
    '/accounts/register/',
    '/accounts/login/',
]

for url in test_urls:
    try:
        response = client.get(url)
        print(f"[{response.status_code}] {url}")
    except Exception as e:
        print(f"[ERROR] {url} -> {e}")

print("\n=== Проверка защищённых страниц ===")
protected_urls = [
    '/equipment/create/',
    '/reports/',
    '/maintenance/create/',
]

for url in protected_urls:
    try:
        response = client.get(url)
        print(f"[{response.status_code}] {url} (должен быть 302 или 403)")
    except Exception as e:
        print(f"[ERROR] {url} -> {e}")

print("\n=== Проверка форм регистрации ===")
from apps.accounts.forms import RegistrationForm

form = RegistrationForm()
print(f"Поля формы регистрации: {list(form.fields.keys())}")
