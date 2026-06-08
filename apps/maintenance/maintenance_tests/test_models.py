"""
Тесты для моделей приложения maintenance.
"""

from django.test import TestCase
from apps.departments.models import Department
from apps.equipment.models import Equipment
from apps.maintenance.models import Maintenance


class MaintenanceModelTest(TestCase):
    """Тесты для модели Maintenance."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.department = Department.objects.create(name='IT-отдел', code='IT')
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use',
            department=self.department
        )
        
        self.maintenance_data = {
            'equipment': self.equipment,
            'type': 'repair',
            'status': 'in_progress',
            'start_date': '2024-01-15',
            'end_date': '2024-01-20',
            'service_provider': 'Сервис-Центр',
            'cost': 15000
        }
    
    def test_create_maintenance(self):
        """Тест создания записи об обслуживании."""
        maintenance = Maintenance.objects.create(**self.maintenance_data)
        
        self.assertEqual(maintenance.equipment, self.equipment)
        self.assertEqual(maintenance.type, 'repair')
        self.assertEqual(maintenance.status, 'in_progress')
        self.assertEqual(maintenance.cost, 15000)
    
    def test_maintenance_string_representation(self):
        """Тест строкового представления."""
        maintenance = Maintenance.objects.create(**self.maintenance_data)
        expected = f"Обслуживание: 000001 - Ноутбук (repair)"
        self.assertEqual(str(maintenance), expected)
    
    def test_maintenance_status_choices(self):
        """Тест выбора статусов."""
        maintenance = Maintenance.objects.create(**self.maintenance_data)
        
        statuses = [choice[0] for choice in Maintenance.STATUS_CHOICES]
        self.assertIn(maintenance.status, statuses)
    
    def test_maintenance_type_choices(self):
        """Тест выбора типов обслуживания."""
        maintenance = Maintenance.objects.create(**self.maintenance_data)
        
        types = [choice[0] for choice in Maintenance.TYPE_CHOICES]
        self.assertIn(maintenance.type, types)
    
    def test_maintenance_without_end_date(self):
        """Тест обслуживания без даты окончания."""
        maintenance = Maintenance.objects.create(
            equipment=self.equipment,
            type='inspection',
            status='in_progress',
            start_date='2024-01-15'
        )
        
        self.assertIsNone(maintenance.end_date)
        self.assertEqual(maintenance.status, 'in_progress')
    
    def test_maintenance_without_cost(self):
        """Тест обслуживания без стоимости."""
        maintenance = Maintenance.objects.create(
            equipment=self.equipment,
            type='inspection',
            status='completed',
            start_date='2024-01-15',
            end_date='2024-01-16'
        )
        
        self.assertIsNone(maintenance.cost)
    
    def test_maintenance_timestamps(self):
        """Тест временных меток."""
        maintenance = Maintenance.objects.create(**self.maintenance_data)
        
        self.assertIsNotNone(maintenance.created_at)
        self.assertIsNotNone(maintenance.updated_at)
    
    def test_maintenance_completed(self):
        """Тест завершённого обслуживания."""
        maintenance = Maintenance.objects.create(
            equipment=self.equipment,
            type='repair',
            status='completed',
            start_date='2024-01-15',
            end_date='2024-01-20'
        )
        
        self.assertEqual(maintenance.status, 'completed')
        self.assertIsNotNone(maintenance.end_date)
    
    def test_maintenance_upcoming(self):
        """Тест запланированного обслуживания."""
        maintenance = Maintenance.objects.create(
            equipment=self.equipment,
            type='inspection',
            status='planned',
            start_date='2030-01-15'
        )
        
        self.assertEqual(maintenance.status, 'planned')