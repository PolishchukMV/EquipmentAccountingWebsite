#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Полная проверка всех страниц сайта на ошибки 404 и 500.
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.test import Client
from django.urls import get_resolver
from apps.accounts.models import CustomUser

# Цвета для вывода
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_section(title):
    print(f"\n{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{title}{RESET}")
    print(f"{CYAN}{'='*70}{RESET}\n")

def get_all_urls():
    """Получить все URL маршруты проекта."""
    from django.urls import reverse, NoReverseMatch
    
    urls_to_test = [
        # Главная и статические страницы
        ('/', 'Главная'),
        ('/about/', 'О системе'),
        ('/help/', 'Помощь'),
        
        # Оборудование
        ('/equipment/', 'Список оборудования'),
        ('/equipment/create/', 'Создание оборудования'),
        ('/equipment/categories/', 'Категории'),
        ('/equipment/categories/1/', 'Детали категории'),
        ('/equipment/1/', 'Детали оборудования'),
        ('/equipment/1/update/', 'Редактирование оборудования'),
        ('/equipment/1/delete/', 'Удаление оборудования'),
        ('/equipment/search/', 'Поиск оборудования'),
        ('/equipment/filter/', 'Фильтрация оборудования'),
        ('/equipment/1/history/', 'История изменений'),
        
        # Подразделения
        ('/departments/', 'Список подразделений'),
        ('/departments/create/', 'Создание подразделения'),
        ('/departments/1/', 'Детали подразделения'),
        ('/departments/1/update/', 'Редактирование подразделения'),
        ('/departments/1/delete/', 'Удаление подразделения'),
        
        # Отчёты
        ('/reports/', 'Дашборд отчётов'),
        ('/reports/inventory/', 'Отчёт по инвентаризации'),
        ('/reports/movement/', 'Отчёт по перемещениям'),
        ('/reports/maintenance/', 'Отчёт по обслуживанию'),
        ('/reports/status/', 'Отчёт по статусам'),
        ('/reports/financial/', 'Финансовый отчёт'),
        ('/reports/history/', 'История отчётов'),
        
        # Обслуживание
        ('/maintenance/', 'Список обслуживания'),
        ('/maintenance/create/', 'Создание обслуживания'),
        ('/maintenance/1/', 'Детали обслуживания'),
        ('/maintenance/1/update/', 'Редактирование обслуживания'),
        ('/maintenance/1/delete/', 'Удаление обслуживания'),
        ('/maintenance/calendar/', 'Календарь обслуживания'),
        
        # Обратная связь
        ('/feedback/', 'Обратная связь'),
        ('/feedback/create/', 'Создание обращения'),
        ('/feedback/1/', 'Детали обращения'),
        
        # Аутентификация
        ('/accounts/login/', 'Вход'),
        ('/accounts/register/', 'Регистрация'),
        ('/accounts/profile/', 'Профиль'),
        ('/accounts/profile/edit/', 'Редактирование профиля'),
        ('/accounts/notifications/', 'Уведомления'),
    ]
    
    return urls_to_test

def setup_test_data():
    """Создание тестовых данных."""
    print_section("ПОДГОТОВКА ТЕСТОВЫХ ДАННЫХ")
    
    from apps.departments.models import Department
    from apps.equipment.models import Category, Equipment
    
    # Создаём отдел
    dept, created = Department.objects.get_or_create(
        name='Test Dept',
        code='TEST',
        defaults={'description': 'Тестовое подразделение'}
    )
    print(f"{'[OK]' if not created else '[INFO]'} Подразделение: {dept.name}")
    
    # Создаём категорию
    category, created = Category.objects.get_or_create(
        name='Test Category',
        code='TEST_CAT',
        defaults={'description': 'Тестовая категория'}
    )
    print(f"{'[OK]' if not created else '[INFO]'} Категория: {category.name}")
    
    # Создаём пользователей
    roles = [
        ('testadmin', 'admin123', 'admin'),
        ('testmanager', 'manager123', 'manager'),
        ('testemployee', 'employee123', 'employee'),
        ('testauditor', 'auditor123', 'auditor'),
    ]
    
    users = {}
    for username, password, role in roles:
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@test.com',
                'role': role,
                'is_active': True,
                'department': dept
            }
        )
        user.set_password(password)
        user.save()
        users[role] = user
        print(f"{'[OK]' if created else '[INFO]'} Пользователь: {username} ({role})")
    
    # Создаём оборудование
    for i in range(1, 4):
        equip, created = Equipment.objects.get_or_create(
            inventory_number=f'TEST_EQ_{i:03d}',
            defaults={
                'name': f'Test Equipment {i}',
                'category': category,
                'serial_number': f'SN_TEST_{i:03d}',
                'manufacturer': 'TestManuf',
                'model': 'TestModel',
                'status': 'in_stock',
                'department': dept
            }
        )
        print(f"{'[OK]' if created else '[INFO]'} Оборудование: {equip.inventory_number}")
    
    return users

def test_urls_anonymous(urls):
    """Тестирование URL без авторизации."""
    print_section("ТЕСТИРОВАНИЕ БЕЗ АВТОРИЗАЦИИ")
    
    client = Client()
    results = {'ok': [], 'redirect': [], 'error': []}
    
    for url, name in urls:
        try:
            response = client.get(url, follow=False)
            if response.status_code == 200:
                results['ok'].append((url, name, 200))
                print(f"{GREEN}[200 OK]{RESET} {name} ({url})")
            elif response.status_code in [301, 302]:
                results['redirect'].append((url, name, response.status_code))
                print(f"{YELLOW}[302 REDIRECT]{RESET} {name} ({url})")
            elif response.status_code == 403:
                results['redirect'].append((url, name, 403))
                print(f"{YELLOW}[403 FORBIDDEN]{RESET} {name} ({url})")
            elif response.status_code == 404:
                results['error'].append((url, name, 404))
                print(f"{RED}[404 NOT FOUND]{RESET} {name} ({url})")
            elif response.status_code == 500:
                results['error'].append((url, name, 500))
                print(f"{RED}[500 SERVER ERROR]{RESET} {name} ({url})")
            else:
                results['error'].append((url, name, response.status_code))
                print(f"{RED}[{response.status_code}]{RESET} {name} ({url})")
        except Exception as e:
            results['error'].append((url, name, 'ERROR'))
            print(f"{RED}[ERROR]{RESET} {name} ({url}): {e}")
    
    return results

def test_urls_authenticated(urls, users):
    """Тестирование URL с авторизацией для разных ролей."""
    print_section("ТЕСТИРОВАНИЕ С АВТОРИЗАЦИЕЙ")
    
    protected_urls = [
        ('/equipment/create/', 'Создание оборудования'),
        ('/reports/', 'Отчёты'),
        ('/accounts/profile/', 'Профиль'),
    ]
    
    all_results = {}
    
    for role, user in users.items():
        print(f"\n{BOLD}{CYAN}Роль: {role.upper()}{RESET}")
        client = Client()
        client.login(username=user.username, password=f'{user.username[4:]}123')
        
        role_results = {'ok': [], 'redirect': [], 'forbidden': [], 'error': []}
        
        for url, name in protected_urls:
            try:
                response = client.get(url, follow=False)
                if response.status_code == 200:
                    role_results['ok'].append((url, name))
                    print(f"  {GREEN}[200 OK]{RESET} {name}")
                elif response.status_code in [301, 302]:
                    role_results['redirect'].append((url, name))
                    print(f"  {YELLOW}[302 REDIRECT]{RESET} {name}")
                elif response.status_code == 403:
                    role_results['forbidden'].append((url, name))
                    print(f"  {YELLOW}[403 FORBIDDEN]{RESET} {name}")
                elif response.status_code == 404:
                    role_results['error'].append((url, name))
                    print(f"  {RED}[404 NOT FOUND]{RESET} {name}")
                elif response.status_code == 500:
                    role_results['error'].append((url, name))
                    print(f"  {RED}[500 ERROR]{RESET} {name}")
                else:
                    role_results['error'].append((url, name))
                    print(f"  {RED}[{response.status_code}]{RESET} {name}")
            except Exception as e:
                role_results['error'].append((url, name))
                print(f"  {RED}[ERROR]{RESET} {name}: {e}")
        
        all_results[role] = role_results
    
    return all_results

def main():
    print(f"\n{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{YELLOW}ПОЛНАЯ ПРОВЕРКА ВСЕХ СТРАНИЦ САЙТА{RESET}")
    print(f"{CYAN}Система учёта оборудования ООО «ПроИнфоСервис»{RESET}")
    print(f"{CYAN}{'='*70}{RESET}\n")
    
    # Подготовка данных
    users = setup_test_data()
    
    # Получаем реальные ID из БД
    from apps.equipment.models import Category, Equipment
    from apps.departments.models import Department
    from apps.maintenance.models import Maintenance
    from apps.feedback.models import FeedbackMessage
    
    category = Category.objects.first()
    dept = Department.objects.first()
    equipment = Equipment.objects.first()
    maintenance = Maintenance.objects.first()
    feedback_msg = FeedbackMessage.objects.first()
    
    if not category or not dept or not equipment:
        print(f"{RED}[ERROR] Не найдены тестовые данные!{RESET}")
        return False
    
    category_id = category.id
    dept_id = dept.id
    equipment_id = equipment.id
    
    # Получаем все URL с реальными ID
    urls = get_all_urls()
    # Обновляем URL с реальными ID
    urls = [
        ('/', 'Главная'),
        ('/about/', 'О системе'),
        ('/help/', 'Помощь'),
        ('/equipment/', 'Список оборудования'),
        ('/equipment/create/', 'Создание оборудования'),
        ('/equipment/categories/', 'Категории'),
        (f'/equipment/categories/{category_id}/', 'Детали категории'),
        (f'/equipment/{equipment_id}/', 'Детали оборудования'),
        (f'/equipment/{equipment_id}/update/', 'Редактирование оборудования'),
        (f'/equipment/{equipment_id}/delete/', 'Удаление оборудования'),
        ('/equipment/search/', 'Поиск оборудования'),
        ('/equipment/filter/', 'Фильтрация оборудования'),
        (f'/equipment/{equipment_id}/history/', 'История изменений'),
        ('/departments/', 'Список подразделений'),
        ('/departments/create/', 'Создание подразделения'),
        (f'/departments/{dept_id}/', 'Детали подразделения'),
        (f'/departments/{dept_id}/update/', 'Редактирование подразделения'),
        (f'/departments/{dept_id}/delete/', 'Удаление подразделения'),
        ('/reports/', 'Дашборд отчётов'),
        ('/reports/inventory/', 'Отчёт по инвентаризации'),
        ('/reports/movement/', 'Отчёт по перемещениям'),
        ('/reports/maintenance/', 'Отчёт по обслуживанию'),
        ('/reports/status/', 'Отчёт по статусам'),
        ('/reports/financial/', 'Финансовый отчёт'),
        ('/reports/history/', 'История отчётов'),
        ('/maintenance/', 'Список обслуживания'),
        ('/maintenance/create/', 'Создание обслуживания'),
    ]
    
    # Добавляем URL с реальными ID если они существуют
    if maintenance:
        maintenance_urls = [
            (f'/maintenance/{maintenance.id}/', 'Детали обслуживания'),
            (f'/maintenance/{maintenance.id}/update/', 'Редактирование обслуживания'),
            (f'/maintenance/{maintenance.id}/delete/', 'Удаление обслуживания'),
        ]
        urls.extend(maintenance_urls)
    else:
        # Создаем тестовое обслуживание для проверки
        from datetime import date
        maintenance = Maintenance.objects.create(
            equipment=equipment,
            maintenance_type='planned',
            description='Test maintenance',
            scheduled_date=date.today(),
            cost=1000,
            contractor='Test Engineer'
        )
        maintenance_urls = [
            (f'/maintenance/{maintenance.id}/', 'Детали обслуживания'),
            (f'/maintenance/{maintenance.id}/update/', 'Редактирование обслуживания'),
            (f'/maintenance/{maintenance.id}/delete/', 'Удаление обслуживания'),
        ]
        urls.extend(maintenance_urls)
    
    urls.extend([
        ('/maintenance/calendar/', 'Календарь обслуживания'),
        ('/feedback/', 'Обратная связь'),
        ('/feedback/create/', 'Создание обращения'),
    ])
    
    if feedback_msg:
        urls.append((f'/feedback/{feedback_msg.id}/', 'Детали обращения'))
    else:
        # Создаем тестовое обращение
        feedback_msg = FeedbackMessage.objects.create(
            subject='Test feedback',
            message='Test message',
            email='test@test.com',
            status='new'
        )
        urls.append((f'/feedback/{feedback_msg.id}/', 'Детали обращения'))
    
    urls.extend([
        ('/accounts/login/', 'Вход'),
        ('/accounts/register/', 'Регистрация'),
        ('/accounts/profile/', 'Профиль'),
        ('/accounts/profile/edit/', 'Редактирование профиля'),
        ('/accounts/notifications/', 'Уведомления'),
    ])
    
    # Тест без авторизации
    anon_results = test_urls_anonymous(urls)
    
    # Тест с авторизацией
    auth_results = test_urls_authenticated(urls, users)
    
    # Итоговый отчёт
    print_section("ИТОГОВЫЙ ОТЧЁТ")
    
    total_errors = len(anon_results['error'])
    for role_results in auth_results.values():
        total_errors += len(role_results['error'])
    
    if total_errors == 0:
        print(f"{GREEN}[OK] ВСЕ СТРАНИЦЫ ДОСТУПНЫ И РАБОТАЮТ КОРРЕКТНО!{RESET}")
    else:
        print(f"{RED}[WARN] НАЙДЕНО {total_errors} ОШИБОК{RESET}")
        print(f"{RED}❌ НАЙДЕНО {total_errors} ОШИБОК{RESET}")
        
        if anon_results['error']:
            print(f"\n{RED}Ошибки для анонимных пользователей:{RESET}")
            for url, name, status in anon_results['error']:
                print(f"  ✗ {name} ({url}): {status}")
        
        for role, role_results in auth_results.items():
            if role_results['error']:
                print(f"\n{RED}Ошибки для роли {role}:{RESET}")
                for url, name in role_results['error']:
                    print(f"  ✗ {name} ({url})")
    
    return total_errors == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
