"""
Тесты для views приложения maintenance.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.departments.models import Department
from apps.equipment.models import Equipment
from apps.maintenance.models import Maintenance


UserModel = get_user_model()


class MaintenanceListViewTest(TestCase):
    """Тесты для списка обслуживания."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.department = Department.objects.create(name='IT-отдел', code='IT')
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use',
            department=self.department
        )
        
        Maintenance.objects.create(
            equipment=self.equipment,
            type='repair',
            status='completed',
            start_date='2024-01-15',
            service_provider='Сервис-Центр'
        )
        
        Maintenance.objects.create(
            equipment=self.equipment,
            type='inspection',
            status='in_progress',
            start_date='2024-02-01'
        )
        
        self.url = reverse('maintenance:maintenance_list')
    
    def test_list_page_loads(self):
        """Тест загрузки страницы списка."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'maintenance/maintenance_list.html')
    
    def test_list_shows_maintenances(self):
        """Тест отображения записей."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Ноутбук')
        self.assertContains(response, 'Сервис-Центр')
    
    def test_list_context(self):
        """Тест контекста страницы списка."""
        response = self.client.get(self.url)
        
        self.assertIn('maintenances', response.context)
        self.assertEqual(len(response.context['maintenances']), 2)


class MaintenanceDetailViewTest(TestCase):
    """Тесты для деталей обслуживания."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.department = Department.objects.create(name='IT-отдел', code='IT')
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use',
            department=self.department
        )
        
        self.maintenance = Maintenance.objects.create(
            equipment=self.equipment,
            type='repair',
            status='in_progress',
            start_date='2024-01-15',
            service_provider='Сервис-Центр',
            cost=15000
        )
        
        self.url = reverse('maintenance:maintenance_detail', kwargs={'pk': self.maintenance.pk})
    
    def test_detail_page_loads(self):
        """Тест загрузки страницы деталей."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'maintenance/maintenance_detail.html')
    
    def test_detail_shows_info(self):
        """Тест отображения информации."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Ноутбук')
        self.assertContains(response, 'Сервис-Центр')
        self.assertContains(response, '15000')
    
    def test_detail_context(self):
        """Тест контекста страницы деталей."""
        response = self.client.get(self.url)
        
        self.assertIn('maintenance', response.context)
        self.assertEqual(response.context['maintenance'], self.maintenance)