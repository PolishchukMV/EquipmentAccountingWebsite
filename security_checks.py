#!/usr/bin/env python
"""
Скрипт для проверки безопасности проекта.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from apps.equipment.models import Equipment
from apps.departments.models import Department

def check_security():
    """Проверка настроек безопасности."""
    issues = []
    warnings = []
    
    print("="*60)
    print("ПРОВЕРКА БЕЗОПАСНОСТИ")
    print("="*60)
    
    # 1. DEBUG режим
    if settings.DEBUG:
        warnings.append("[!] DEBUG = True (не рекомендуется для production)")
    else:
        print("[OK] DEBUG = False")
    
    # 2. SECRET_KEY
    if settings.SECRET_KEY.startswith('django-insecure-'):
        warnings.append("[!] SECRET_KEY использует insecure-значение")
    else:
        print("[OK] SECRET_KEY настроен")
    
    # 3. ALLOWED_HOSTS
    if '*' in settings.ALLOWED_HOSTS:
        issues.append("[CRITICAL] ALLOWED_HOSTS = ['*'] (опасно для production)")
    else:
        print(f"[OK] ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # 4. CSRF
    if hasattr(settings, 'CSRF_COOKIE_SECURE'):
        if settings.CSRF_COOKIE_SECURE:
            print("[OK] CSRF_COOKIE_SECURE = True")
        else:
            warnings.append("[!] CSRF_COOKIE_SECURE = False")
    else:
        print("[OK] CSRF включён по умолчанию")
    
    # 5. SESSION_COOKIE_SECURE
    if hasattr(settings, 'SESSION_COOKIE_SECURE'):
        if settings.SESSION_COOKIE_SECURE:
            print("[OK] SESSION_COOKIE_SECURE = True")
        else:
            warnings.append("[!] SESSION_COOKIE_SECURE = False")
    
    # 6. SECURE_BROWSER_XSS_FILTER
    if hasattr(settings, 'SECURE_BROWSER_XSS_FILTER'):
        if settings.SECURE_BROWSER_XSS_FILTER:
            print("[OK] SECURE_BROWSER_XSS_FILTER = True")
    
    # 7. SECURE_CONTENT_TYPE_NOSNIFF
    if hasattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF'):
        if settings.SECURE_CONTENT_TYPE_NOSNIFF:
            print("[OK] SECURE_CONTENT_TYPE_NOSNIFF = True")
    
    # 8. X_FRAME_OPTIONS
    if hasattr(settings, 'X_FRAME_OPTIONS'):
        if settings.X_FRAME_OPTIONS == 'DENY' or settings.X_FRAME_OPTIONS == 'SAMEORIGIN':
            print(f"[OK] X_FRAME_OPTIONS = {settings.X_FRAME_OPTIONS}")
        else:
            warnings.append(f"[!] X_FRAME_OPTIONS = {settings.X_FRAME_OPTIONS}")
    
    # 9. Проверка паролей
    print("\n--- Проверка пользователей ---")
    User = get_user_model()
    total_users = User.objects.count()
    superusers = User.objects.filter(is_superuser=True).count()
    staff = User.objects.filter(is_staff=True).count()
    
    print(f"[OK] Всего пользователей: {total_users}")
    print(f"[OK] Суперпользователи: {superusers}")
    print(f"[OK] Персонал: {staff}")
    
    if superusers == 0:
        issues.append("[CRITICAL] Нет суперпользователей")
    elif superusers > 3:
        warnings.append(f"[!] Много суперпользователей: {superusers}")
    
    # 10. Проверка оборудования
    print("\n--- Проверка данных ---")
    total_equipment = Equipment.objects.count()
    print(f"[OK] Всего оборудования: {total_equipment}")
    
    total_departments = Department.objects.count()
    print(f"[OK] Всего подразделений: {total_departments}")
    
    # 11. Проверка файлов
    print("\n--- Проверка файлов ---")
    
    # Проверка .env
    if os.path.exists('.env'):
        print("[OK] Файл .env существует")
    else:
        warnings.append("[!] Файл .env не найден")
    
    # Проверка .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore = f.read()
            if 'db.sqlite3' in gitignore:
                print("[OK] db.sqlite3 в .gitignore")
            else:
                warnings.append("[!] db.sqlite3 не в .gitignore")
            
            if '.env' in gitignore:
                print("[OK] .env в .gitignore")
            else:
                issues.append("[CRITICAL] .env не в .gitignore")
    
    # Вывод результатов
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ")
    print("="*60)
    
    if issues:
        print("\n[CRITICAL] КРИТИЧЕСКИЕ ПРОБЛЕМЫ:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n[WARNING] ПРЕДУПРЕЖДЕНИЯ:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not issues and not warnings:
        print("\n[OK] Все проверки пройдены успешно!")
    
    print("\n" + "="*60)
    
    return len(issues) == 0


if __name__ == '__main__':
    success = check_security()
    sys.exit(0 if success else 1)