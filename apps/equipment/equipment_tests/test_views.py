"""
Тесты для views приложения equipment.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.departments.models import Department
from apps.equipment.models import Category, Equipment


UserModel = get_user_model()


class EquipmentListViewTest(TestCase):
    """Тесты для списка оборудования."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.category = Category.objects.create(name='Компьютеры', code='COMP')
        
        self.equipment1 = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук 1',
            category=self.category,
            status='in_use'
        )
        
        self.equipment2 = Equipment.objects.create(
            inventory_number='000002',
            name='Ноутбук 2',
            category=self.category,
            status='in_stock'
        )
        
        self.url = reverse('equipment:equipment_list')
    
    def test_list_page_loads(self):
        """Тест загрузки страницы списка."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/equipment_list.html')
    
    def test_list_shows_equipment(self):
        """Тест отображения оборудования."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Ноутбук 1')
        self.assertContains(response, 'Ноутбук 2')
    
    def test_list_context(self):
        """Тест контекста страницы списка."""
        response = self.client.get(self.url)
        
        self.assertIn('equipment_list', response.context)
        self.assertEqual(len(response.context['equipment_list']), 2)


class EquipmentDetailViewTest(TestCase):
    """Тесты для деталей оборудования."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.category = Category.objects.create(name='Компьютеры', code='COMP')
        
        self.equipment = Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук Dell',
            category=self.category,
            status='in_use',
            serial_number='SN123',
            manufacturer='Dell',
            model='Latitude',
            purchase_price=85000,
            location='Кабинет 301'
        )
        
        self.url = reverse('equipment:equipment_detail', kwargs={'pk': self.equipment.pk})
    
    def test_detail_page_loads(self):
        """Тест загрузки страницы деталей."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/equipment_detail.html')
    
    def test_detail_shows_info(self):
        """Тест отображения информации."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Ноутбук Dell')
        self.assertContains(response, '000001')
        self.assertContains(response, 'Dell')
    
    def test_detail_context(self):
        """Тест контекста страницы деталей."""
        response = self.client.get(self.url)
        
        self.assertIn('equipment', response.context)
        self.assertEqual(response.context['equipment'], self.equipment)


class EquipmentSearchViewTest(TestCase):
    """Тесты для поиска оборудования."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.category = Category.objects.create(name='Компьютеры', code='COMP')
        
        Equipment.objects.create(
            inventory_number='000001',
            name='Ноутбук Dell',
            category=self.category,
            status='in_use',
            serial_number='SN123'
        )
        
        Equipment.objects.create(
            inventory_number='000002',
            name='Ноутбук HP',
            category=self.category,
            status='in_use',
            serial_number='SN456'
        )
        
        self.url = reverse('equipment:equipment_search')
    
    def test_search_by_inventory_number(self):
        """Тест поиска по инвентарному номеру."""
        response = self.client.get(self.url, {'q': '000001'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ноутбук Dell')
        self.assertNotContains(response, 'Ноутбук HP')
    
    def test_search_by_name(self):
        """Тест поиска по названию."""
        response = self.client.get(self.url, {'q': 'HP'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ноутбук HP')
    
    def test_search_no_results(self):
        """Тест поиска без результатов."""
        response = self.client.get(self.url, {'q': 'NONEXISTENT'})
        
        self.assertEqual(response.status_code, 200)


class EquipmentFilterViewTest(TestCase):
    """Тесты для фильтрации оборудования."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
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
            status='in_stock'
        )
        
        self.url = reverse('equipment:equipment_filter')
    
    def test_filter_by_status(self):
        """Тест фильтрации по статусу."""
        response = self.client.get(self.url, {'status': 'in_use'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ноутбук 1')
        self.assertNotContains(response, 'Ноутбук 2')
    
    def test_filter_by_category(self):
        """Тест фильтрации по категории."""
        response = self.client.get(self.url, {'category': self.category.pk})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ноутбук 1')
        self.assertContains(response, 'Ноутбук 2')