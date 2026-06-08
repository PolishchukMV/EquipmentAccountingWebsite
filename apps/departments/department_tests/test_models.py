"""
Тесты для моделей приложения departments.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.departments.models import Department, Employee


UserModel = get_user_model()


class DepartmentModelTest(TestCase):
    """Тесты для модели Department."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.parent_dept = Department.objects.create(
            name='Главный офис',
            code='HEAD',
            description='Центральный офис компании'
        )
        
        self.child_dept = Department.objects.create(
            name='IT-отдел',
            code='IT',
            description='Отдел информационных технологий',
            parent=self.parent_dept
        )
        
        self.manager = UserModel.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='pass123',
            role=UserModel.ROLE_CHOICES[1][0]
        )
    
    def test_create_department(self):
        """Тест создания подразделения."""
        dept = Department.objects.create(
            name='Бухгалтерия',
            code='ACCT'
        )
        
        self.assertEqual(dept.name, 'Бухгалтерия')
        self.assertEqual(dept.code, 'ACCT')
        self.assertIsNone(dept.parent)
        self.assertIsNone(dept.head)
    
    def test_department_with_parent(self):
        """Тест подразделения с родителем."""
        self.assertEqual(self.child_dept.parent, self.parent_dept)
    
    def test_department_with_head(self):
        """Тест подразделения с руководителем."""
        self.parent_dept.head = self.manager
        self.parent_dept.save()
        
        self.assertEqual(self.parent_dept.head, self.manager)
    
    def test_department_string_representation(self):
        """Тест строкового представления подразделения."""
        dept = Department.objects.create(name='Тестовый отдел', code='TEST')
        self.assertEqual(str(dept), 'Тестовый отдел')
    
    def test_department_code_unique(self):
        """Тест уникальности кода подразделения."""
        Department.objects.create(name='Отдел 1', code='DEPT1')
        
        with self.assertRaises(Exception):
            Department.objects.create(name='Отдел 2', code='DEPT1')
    
    def test_department_hierarchy(self):
        """Тест иерархии подразделений."""
        level1 = Department.objects.create(name='Уровень 1', code='L1')
        level2 = Department.objects.create(name='Уровень 2', code='L2', parent=level1)
        level3 = Department.objects.create(name='Уровень 3', code='L3', parent=level2)
        
        self.assertEqual(level2.parent, level1)
        self.assertEqual(level3.parent, level2)
    
    def test_department_get_employee_count(self):
        """Тест подсчета сотрудников в подразделении."""
        dept = Department.objects.create(name='Отдел', code='TEST')
        
        employee1 = Employee.objects.create(
            user=UserModel.objects.create_user(
                username='emp1',
                email='emp1@example.com',
                password='pass',
                department=dept
            ),
            department=dept,
            position='Сотрудник'
        )
        
        employee2 = Employee.objects.create(
            user=UserModel.objects.create_user(
                username='emp2',
                email='emp2@example.com',
                password='pass',
                department=dept
            ),
            department=dept,
            position='Сотрудник'
        )
        
        self.assertEqual(dept.get_employee_count(), 2)
    
    def test_department_empty(self):
        """Тест подразделения без сотрудников."""
        dept = Department.objects.create(name='Пустой отдел', code='EMPTY')
        self.assertEqual(dept.get_employee_count(), 0)
    
    def test_timestamps(self):
        """Тест временных меток."""
        dept = Department.objects.create(name='Отдел', code='TEST')
        
        self.assertIsNotNone(dept.created_at)
        self.assertIsNotNone(dept.updated_at)


class EmployeeModelTest(TestCase):
    """Тесты для модели Employee."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.department = Department.objects.create(
            name='IT-отдел',
            code='IT'
        )
        
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            department=self.department
        )
        
        self.employee_data = {
            'user': self.user,
            'department': self.department,
            'position': 'Разработчик',
            'employee_id': 'EMP001',
            'hire_date': '2024-01-15'
        }
    
    def test_create_employee(self):
        """Тест создания сотрудника."""
        employee = Employee.objects.create(**self.employee_data)
        
        self.assertEqual(employee.user, self.user)
        self.assertEqual(employee.department, self.department)
        self.assertEqual(employee.position, 'Разработчик')
        self.assertEqual(employee.employee_id, 'EMP001')
    
    def test_employee_string_representation(self):
        """Тест строкового представления сотрудника."""
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(str(employee), 'Иван Иванов - Разработчик')
    
    def test_employee_without_user(self):
        """Тест сотрудника без пользователя."""
        employee = Employee.objects.create(
            department=self.department,
            position='Внешний консультант',
            employee_id='EXT001'
        )
        
        self.assertIsNone(employee.user)
        self.assertEqual(employee.position, 'Внешний консультант')
    
    def test_employee_timestamps(self):
        """Тест временных меток сотрудника."""
        employee = Employee.objects.create(**self.employee_data)
        
        self.assertIsNotNone(employee.created_at)
        self.assertIsNotNone(employee.updated_at)