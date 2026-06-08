"""
Тесты для views приложения departments.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.departments.models import Department


UserModel = get_user_model()


class DepartmentListViewTest(TestCase):
    """Тесты для списка подразделений."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.department1 = Department.objects.create(name='Отдел 1', code='DEPT1')
        self.department2 = Department.objects.create(name='Отдел 2', code='DEPT2')
        self.url = reverse('departments:department_list')
    
    def test_list_page_loads(self):
        """Тест загрузки страницы списка."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'departments/department_list.html')
    
    def test_list_shows_departments(self):
        """Тест отображения подразделений."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Отдел 1')
        self.assertContains(response, 'Отдел 2')
    
    def test_list_context(self):
        """Тест контекста страницы списка."""
        response = self.client.get(self.url)
        
        self.assertIn('departments', response.context)
        self.assertEqual(len(response.context['departments']), 2)


class DepartmentDetailViewTest(TestCase):
    """Тесты для деталей подразделения."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.department = Department.objects.create(
            name='IT-отдел',
            code='IT',
            description='Отдел информационных технологий'
        )
        self.url = reverse('departments:department_detail', kwargs={'pk': self.department.pk})
    
    def test_detail_page_loads(self):
        """Тест загрузки страницы деталей."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'departments/department_detail.html')
    
    def test_detail_shows_info(self):
        """Тест отображения информации о подразделении."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'IT-отдел')
        self.assertContains(response, 'Отдел информационных технологий')