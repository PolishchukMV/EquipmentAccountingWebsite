"""
Тесты для URL маршрутов приложения equipment.
"""

from django.test import TestCase
from django.urls import reverse, resolve
from apps.equipment import views


class EquipmentURLTest(TestCase):
    """Тесты URL маршрутов оборудования."""
    
    def test_equipment_list_url(self):
        """Тест URL списка оборудования."""
        url = reverse('equipment:equipment_list')
        self.assertEqual(url, '/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentListView)
    
    def test_equipment_create_url(self):
        """Тест URL создания оборудования."""
        url = reverse('equipment:equipment_create')
        self.assertEqual(url, '/create/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentCreateView)
    
    def test_equipment_detail_url(self):
        """Тест URL деталей оборудования."""
        url = reverse('equipment:equipment_detail', kwargs={'pk': 1})
        self.assertEqual(url, '/1/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentDetailView)
    
    def test_equipment_update_url(self):
        """Тест URL редактирования оборудования."""
        url = reverse('equipment:equipment_update', kwargs={'pk': 1})
        self.assertEqual(url, '/1/update/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentUpdateView)
    
    def test_equipment_delete_url(self):
        """Тест URL удаления оборудования."""
        url = reverse('equipment:equipment_delete', kwargs={'pk': 1})
        self.assertEqual(url, '/1/delete/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentDeleteView)
    
    def test_equipment_search_url(self):
        """Тест URL поиска оборудования."""
        url = reverse('equipment:equipment_search')
        self.assertEqual(url, '/search/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentSearchView)
    
    def test_equipment_filter_url(self):
        """Тест URL фильтрации оборудования."""
        url = reverse('equipment:equipment_filter')
        self.assertEqual(url, '/filter/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentFilterView)
    
    def test_equipment_status_url(self):
        """Тест URL изменения статуса."""
        url = reverse('equipment:equipment_status', kwargs={'pk': 1})
        self.assertEqual(url, '/1/status/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentStatusView)
    
    def test_category_list_url(self):
        """Тест URL списка категорий."""
        url = reverse('equipment:category_list')
        self.assertEqual(url, '/categories/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.CategoryListView)
    
    def test_category_detail_url(self):
        """Тест URL деталей категории."""
        url = reverse('equipment:category_detail', kwargs={'pk': 1})
        self.assertEqual(url, '/categories/1/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.CategoryDetailView)
    
    def test_equipment_history_url(self):
        """Тест URL истории оборудования."""
        url = reverse('equipment:equipment_history', kwargs={'pk': 1})
        self.assertEqual(url, '/1/history/')
        
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, views.EquipmentHistoryView)