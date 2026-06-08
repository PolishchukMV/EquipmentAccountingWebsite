"""
Тесты для views приложения reports.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.departments.models import Department
from apps.equipment.models import Category, Equipment
from apps.maintenance.models import Maintenance


UserModel = get_user_model()


class ReportsDashboardViewTest(TestCase):
    """Тесты для дашборда отчётов."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.url = reverse('reports:reports_dashboard')
    
    def test_dashboard_requires_login(self):
        """Тест, что дашборд требует авторизации."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_dashboard_page_loads(self):
        """Тест загрузки дашборда."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/reports_dashboard.html')


class InventoryReportViewTest(TestCase):
    """Тесты для отчёта по оборудованию."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.category = Category.objects.create(name='Компьютеры', code='COMP')
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук Dell',
            category=self.category,
            status='in_use',
            manufacturer='Dell',
            model='Latitude',
            purchase_price=85000
        )
        
        self.url = reverse('reports:inventory_report')
    
    def test_report_requires_login(self):
        """Тест, что отчёт требует авторизации."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_inventory_report_html(self):
        """Тест HTML версии отчёта."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/inventory_report.html')
        self.assertContains(response, 'Ноутбук Dell')
    
    def test_inventory_report_xlsx(self):
        """Тест экспорта в Excel."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url, {'format': 'xlsx'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=equipment_report.xlsx')
    
    def test_inventory_report_docx(self):
        """Тест экспорта в Word."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url, {'format': 'docx'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )


class MovementReportViewTest(TestCase):
    """Тесты для отчёта по перемещениям."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.user = UserModel.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.url = reverse('reports:movement_report')
    
    def test_movement_report_requires_login(self):
        """Тест, что отчёт требует авторизации."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_movement_report_html(self):
        """Тест HTML версии отчёта."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/movement_report.html')


class MaintenanceReportViewTest(TestCase):
    """Тесты для отчёта по обслуживанию."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.user = UserModel.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
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
            status='completed',
            start_date='2024-01-15',
            service_provider='Сервис-Центр',
            cost=15000
        )
        
        self.url = reverse('reports:maintenance_report')
    
    def test_maintenance_report_requires_login(self):
        """Тест, что отчёт требует авторизации."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_maintenance_report_shows_data(self):
        """Тест отображения данных отчёта."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ноутбук')
        self.assertContains(response, '15000')


class StatusReportViewTest(TestCase):
    """Тесты для отчёта по статусам."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.user = UserModel.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.category = Category.objects.create(name='Компьютеры', code='COMP')
        
        Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук 1',
            category=self.category,
            status='in_use'
        )
        
        Equipment.objects.create(
            inventory_number='000002',
            name='Ноутбук 2',
            category=self.category,
            status='in_use'
        )
        
        Equipment.objects.create(
            inventory_number='000003',
            name='Ноутбук 3',
            category=self.category,
            status='in_stock'
        )
        
        self.url = reverse('reports:status_report')
    
    def test_status_report_requires_login(self):
        """Тест, что отчёт требует авторизации."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_status_report_shows_stats(self):
        """Тест статистики статусов."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'in_use')
        self.assertContains(response, 'in_stock')


class FinancialReportViewTest(TestCase):
    """Тесты для финансового отчёта."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.user = UserModel.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.department = Department.objects.create(name='IT-отдел', code='IT')
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук',
            status='in_use',
            department=self.department,
            purchase_price=85000
        )
        
        self.maintenance = Maintenance.objects.create(
            equipment=self.equipment,
            type='repair',
            status='completed',
            start_date='2024-01-15',
            cost=15000
        )
        
        self.url = reverse('reports:financial_report')
    
    def test_financial_report_requires_login(self):
        """Тест, что отчёт требует авторизации."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')
    
    def test_financial_report_calculations(self):
        """Тест расчётов финансового отчёта."""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '85000')
        self.assertContains(response, '15000')