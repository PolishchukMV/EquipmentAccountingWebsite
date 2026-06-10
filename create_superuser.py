#!/usr/bin/env python
"""
Скрипт для создания суперпользователя (администратора).
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Данные администратора
admin_data = {
    'username': 'admin',
    'email': 'admin@example.com',
    'first_name': 'Администратор',
    'last_name': 'Системы',
    'password': 'admin123',
}

# Проверка, существует ли пользователь
if User.objects.filter(username=admin_data['username']).exists():
    print(f"[INFO] Пользователь '{admin_data['username']}' уже существует")
    admin = User.objects.get(username=admin_data['username'])
else:
    # Создание суперпользователя
    admin = User.objects.create_superuser(
        username=admin_data['username'],
        email=admin_data['email'],
        first_name=admin_data['first_name'],
        last_name=admin_data['last_name'],
        password=admin_data['password'],
    )
    print(f"[OK] Суперпользователь '{admin_data['username']}' успешно создан")

# Сохраняем скрипт для будущих ссылок
print("\n[INFO] Сохраните эти данные в безопасном месте!")
print("[INFO] Скрипт create_superuser.py можно запустить повторно для проверки")

# Вывод информации
print("\n" + "="*50)
print("ДАННЫЕ ДЛЯ ВХОДА В АДМИН-ПАНЕЛЬ")
print("="*50)
print(f"URL: http://localhost:8000/admin/")
print(f"Имя пользователя: {admin.username}")
print(f"Пароль: {admin_data['password']}")
print(f"Email: {admin.email}")
print(f"Имя: {admin.first_name} {admin.last_name}")
print("="*50)
print("\n[WARNING] Пожалуйста, измените пароль после первого входа!")
print("="*50)