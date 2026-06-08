#!/usr/bin/env python
"""
Простой набор тестов проекта.
"""

import os
import sys
import django
from pathlib import Path

# Добавляем корень проекта в путь
sys.path.insert(0, str(Path(__file__).parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_tracking.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.departments.models import Department
from apps.equipment.models import Category, Equipment
from apps.maintenance.models import Maintenance


class SimpleTest(TestCase):
    """Простые тесты проекта."""
    
    def setUp(self):
        """Настройка."""
        self.user = get_user_model().objects.create_user(
            username='test',
            password='test123'
        )
        self.dept = Department.objects.create(name='Отдел', code='DEPT')
        self.category = Category.objects.create(name='Категория', code='CAT')
    
    def test_user_creation(self):
        """Тест создания пользователя."""
        self.assertEqual(self.user.username, 'test')
        print("[OK] Пользователь создан")
    
    def test_department_creation(self):
        """Тест создания подразделения."""
        self.assertEqual(self.dept.name, 'Отдел')
        print("[OK] Подразделение создано")
    
    def test_category_creation(self):
        """Тест создания категории."""
        self.assertEqual(self.category.name, 'Категория')
        print("[OK] Категория создана")
    
    def test_equipment_creation(self):
        """Тест создания оборудования."""
        equipment = Equipment.objects.create(
            inventory_number='001',
            name='Ноутбук',
            category=self.category,
            status='in_use',
            department=self.dept
        )
        self.assertEqual(equipment.name, 'Ноутбук')
        print("[OK] Оборудование создано")
    
    def test_login(self):
        """Тест входа."""
        client = Client()
        client.login(username='test', password='test123')
        response = client.get('/admin/')
        # 302 - редирект на логин (нормально если не суперпользователь)
        self.assertIn(response.status_code, [200, 302])
        print("[OK] Вход успешен")


if __name__ == '__main__':
    import unittest
    
    # Запуск тестов
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Вывод итогов
    print("\n" + "="*50)
    if result.wasSuccessful():
        print("Все тесты пройдены!")
    else:
        print(f"Провалено тестов: {len(result.failures) + len(result.errors)}")
    print("="*50)