"""
Тесты для views сотрудников.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Employee, Department

UserModel = get_user_model()


class EmployeeViewTest(TestCase):
    """Тесты для представлений сотрудников."""
    
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
        self.employee_user = UserModel.objects.create_user(
            username='john_doe',
            password='john123',
            role='employee'
        )
        
        # Создаём подразделение
        self.department = Department.objects.create(
            name='IT отдел',
            code='IT'
        )
        
        self.client = Client()
    
    def test_employee_list_requires_login(self):
        """Тест, что список сотрудников требует авторизации."""
        response = self.client.get(reverse('departments:employee_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_employee_list_manager_access(self):
        """Тест доступа менеджера к списку сотрудников."""
        self.client.login(username='manager', password='manager123')
        response = self.client.get(reverse('departments:employee_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_employee_create_get(self):
        """Тест отображения формы создания сотрудника."""
        self.client.login(username='manager', password='manager123')
        response = self.client.get(reverse('departments:employee_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_employee_create_post(self):
        """Тест создания сотрудника."""
        self.client.login(username='manager', password='manager123')
        
        response = self.client.post(reverse('departments:employee_create'), {
            'username': 'john_doe',
            'department': self.department.pk,
            'position': 'Разработчик',
            'employee_id': 'EMP001',
            'hire_date': '2024-01-15',
            'is_active': True,
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Employee.objects.filter(employee_id='EMP001').exists())
    
    def test_employee_create_duplicate_user(self):
        """Тест создания дубликата сотрудника."""
        self.client.login(username='manager', password='manager123')
        
        # Создаём первого сотрудника
        Employee.objects.create(
            user=self.employee_user,
            department=self.department,
            position='Разработчик',
            employee_id='EMP001',
            hire_date='2024-01-15',
        )
        
        # Пытаемся создать второго с тем же пользователем
        response = self.client.post(reverse('departments:employee_create'), {
            'username': 'john_doe',
            'department': self.department.pk,
            'position': 'Аналитик',
            'employee_id': 'EMP002',
            'hire_date': '2024-01-15',
        })
        
        self.assertEqual(response.status_code, 200)  # Форма с ошибкой
        self.assertFormError(response.context['form'], 'username', 'У этого пользователя уже есть запись сотрудника.')
    
    def test_employee_detail(self):
        """Тест просмотра деталей сотрудника."""
        self.client.login(username='manager', password='manager123')
        
        employee = Employee.objects.create(
            user=self.employee_user,
            department=self.department,
            position='Разработчик',
            employee_id='EMP001',
            hire_date='2024-01-15',
        )
        
        response = self.client.get(reverse('departments:employee_detail', kwargs={'pk': employee.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_employee_update(self):
        """Тест редактирования сотрудника."""
        self.client.login(username='manager', password='manager123')
        
        employee = Employee.objects.create(
            user=self.employee_user,
            department=self.department,
            position='Разработчик',
            employee_id='EMP001',
            hire_date='2024-01-15',
        )
        
        response = self.client.post(reverse('departments:employee_update', kwargs={'pk': employee.pk}), {
            'username': 'john_doe',
            'department': self.department.pk,
            'position': 'Старший разработчик',
            'employee_id': 'EMP001',
            'hire_date': '2024-01-15',
            'is_active': True,
        })
        
        self.assertEqual(response.status_code, 302)
        
        employee.refresh_from_db()
        self.assertEqual(employee.position, 'Старший разработчик')
    
    def test_employee_delete(self):
        """Тест удаления сотрудника."""
        self.client.login(username='manager', password='manager123')
        
        employee = Employee.objects.create(
            user=self.employee_user,
            department=self.department,
            position='Разработчик',
            employee_id='EMP001',
            hire_date='2024-01-15',
        )
        
        response = self.client.post(reverse('departments:employee_delete', kwargs={'pk': employee.pk}))
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(pk=employee.pk).exists())
