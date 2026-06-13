"""
Тесты для views назначений оборудования.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Equipment, Assignment
from apps.departments.models import Department

UserModel = get_user_model()


class AssignmentViewTest(TestCase):
    """Тесты для представлений назначений."""
    
    def setUp(self):
        """Настройка тестов."""
        # Создаём пользователей
        self.admin = UserModel.objects.create_user(
            username='admin',
            password='admin123',
            role='admin'
        )
        self.manager = UserModel.objects.create_user(
            username='manager',
            password='manager123',
            role='manager'
        )
        self.employee = UserModel.objects.create_user(
            username='employee',
            password='employee123',
            role='employee'
        )
        
        # Создаём подразделение и оборудование
        self.department = Department.objects.create(
            name='IT отдел',
            code='IT'
        )
        
        self.equipment = Equipment.objects.create(
            inventory_number='TEST001',
            name='Тестовый ноутбук',
            status='available'
        )
        
        self.client = Client()
    
    def test_assignment_list_requires_login(self):
        """Тест, что список назначений требует авторизации."""
        response = self.client.get(reverse('equipment:assignment_list'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_assignment_list_manager_access(self):
        """Тест доступа менеджера к списку назначений."""
        self.client.login(username='manager', password='manager123')
        response = self.client.get(reverse('equipment:assignment_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_assignment_create_get(self):
        """Тест отображения формы создания назначения."""
        self.client.login(username='manager', password='manager123')
        response = self.client.get(reverse('equipment:assignment_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_assignment_create_post(self):
        """Тест создания назначения."""
        self.client.login(username='manager', password='manager123')
        
        response = self.client.post(reverse('equipment:assignment_create'), {
            'equipment': self.equipment.pk,
            'to_department': self.department.pk,
            'reason': 'Тестовое назначение',
        })
        
        self.assertEqual(response.status_code, 302)  # Редирект после успеха
        self.assertTrue(Assignment.objects.filter(equipment=self.equipment).exists())
        
        # Проверяем, что статус оборудования изменился
        self.equipment.refresh_from_db()
        self.assertEqual(self.equipment.status, 'in_use')
    
    def test_assignment_detail(self):
        """Тест просмотра деталей назначения."""
        self.client.login(username='manager', password='manager123')
        
        assignment = Assignment.objects.create(
            equipment=self.equipment,
            to_department=self.department,
            reason='Тест',
            created_by=self.manager
        )
        
        response = self.client.get(reverse('equipment:assignment_detail', kwargs={'pk': assignment.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_assignment_return(self):
        """Тест возврата оборудования."""
        self.client.login(username='manager', password='manager123')
        
        assignment = Assignment.objects.create(
            equipment=self.equipment,
            to_department=self.department,
            reason='Тест',
            status='active',
            created_by=self.manager
        )
        
        response = self.client.post(reverse('equipment:assignment_return', kwargs={'pk': assignment.pk}))
        
        self.assertEqual(response.status_code, 302)
        
        # Проверяем статусы
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, 'returned')
        
        self.equipment.refresh_from_db()
        self.assertEqual(self.equipment.status, 'available')
    
    def test_my_assignments(self):
        """Тест просмотра моих назначений."""
        self.client.login(username='employee', password='employee123')
        
        Assignment.objects.create(
            equipment=self.equipment,
            to_person=self.employee,
            reason='Тест',
            status='active',
            created_by=self.manager
        )
        
        response = self.client.get(reverse('equipment:my_assignments'))
        self.assertEqual(response.status_code, 200)
