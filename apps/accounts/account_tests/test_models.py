"""
Тесты для моделей приложения accounts.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from apps.departments.models import Department
from apps.accounts.models import Notification


UserModel = get_user_model()


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.department = Department.objects.create(
            name='IT-отдел',
            code='IT'
        )
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'role': UserModel.ROLE_CHOICES[0][0],
            'phone': '+79001234567',
            'department': self.department
        }
    
    def test_create_user(self):
        """Тест создания обычного пользователя."""
        user = UserModel.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Иван')
        self.assertEqual(user.last_name, 'Иванов')
        self.assertEqual(user.role, UserModel.ROLE_CHOICES[0][0])
        self.assertEqual(user.phone, '+79001234567')
        self.assertEqual(user.department, self.department)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Тест создания суперпользователя."""
        superuser = UserModel.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertEqual(superuser.username, 'admin')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
    
    def test_user_string_representation(self):
        """Тест строкового представления пользователя."""
        user = UserModel.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_user_full_name(self):
        """Тест получения полного имени пользователя."""
        user = UserModel.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'Иван Иванов')
    
    def test_user_role_choices(self):
        """Тест выбора ролей пользователя."""
        user = UserModel.objects.create_user(**self.user_data)
        
        # Проверка всех возможных ролей
        roles = [choice[0] for choice in UserModel.ROLE_CHOICES]
        self.assertIn(user.role, roles)
    
    def test_user_timestamps(self):
        """Тест временных меток пользователя."""
        user = UserModel.objects.create_user(**self.user_data)
        
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)
        self.assertLess(user.created_at, timezone.now() + timedelta(seconds=1))
    
    def test_user_email_unique(self):
        """Тест уникальности email."""
        UserModel.objects.create_user(**self.user_data)
        
        with self.assertRaises(Exception):
            UserModel.objects.create_user(
                username='anotheruser',
                email='test@example.com',
                password='pass123'
            )
    
    def test_user_username_unique(self):
        """Тест уникальности username."""
        UserModel.objects.create_user(**self.user_data)
        
        with self.assertRaises(Exception):
            UserModel.objects.create_user(
                username='testuser',
                email='another@example.com',
                password='pass123'
            )
    
    def test_user_manager_role(self):
        """Тест создания менеджера."""
        manager = UserModel.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='pass123',
            role=UserModel.ROLE_CHOICES[1][0]
        )
        
        self.assertEqual(manager.role, UserModel.ROLE_CHOICES[1][0])
        self.assertTrue(manager.is_manager)
    
    def test_user_employee_role(self):
        """Тест создания сотрудника."""
        employee = UserModel.objects.create_user(
            username='employee',
            email='employee@example.com',
            password='pass123',
            role=UserModel.ROLE_CHOICES[2][0]
        )
        
        self.assertEqual(employee.role, UserModel.ROLE_CHOICES[2][0])
        self.assertTrue(employee.is_employee)


class NotificationModelTest(TestCase):
    """Тесты для модели Notification."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.notification_data = {
            'user': self.user,
            'message': 'Тестовое уведомление',
            'notification_type': Notification.NOTIFICATION_CHOICES[0][0],
            'is_read': False
        }
    
    def test_create_notification(self):
        """Тест создания уведомления."""
        notification = Notification.objects.create(**self.notification_data)
        
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, 'Тестовое уведомление')
        self.assertFalse(notification.is_read)
    
    def test_notification_string_representation(self):
        """Тест строкового представления уведомления."""
        notification = Notification.objects.create(**self.notification_data)
        expected_str = f"Уведомление для {self.user.username}: Тестовое уведомление"
        self.assertEqual(str(notification), expected_str)
    
    def test_notification_mark_as_read(self):
        """Тест отметки уведомления как прочитанного."""
        notification = Notification.objects.create(**self.notification_data)
        
        notification.is_read = True
        notification.save()
        
        self.assertTrue(notification.is_read)
    
    def test_notification_types(self):
        """Тест типов уведомлений."""
        notification = Notification.objects.create(**self.notification_data)
        
        types = [choice[0] for choice in Notification.NOTIFICATION_CHOICES]
        self.assertIn(notification.notification_type, types)
    
    def test_unread_notifications_for_user(self):
        """Тест получения непрочитанных уведомлений пользователя."""
        Notification.objects.create(
            user=self.user,
            message='Уведомление 1',
            notification_type='info'
        )
        Notification.objects.create(
            user=self.user,
            message='Уведомление 2',
            notification_type='warning'
        )
        read_notification = Notification.objects.create(
            user=self.user,
            message='Уведомление 3',
            notification_type='info',
            is_read=True
        )
        
        unread_count = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).count()
        
        self.assertEqual(unread_count, 2)
    
    def test_user_notifications_ordered(self):
        """Тест сортировки уведомлений по дате."""
        notification1 = Notification.objects.create(
            user=self.user,
            message='Первое',
            notification_type='info'
        )
        notification2 = Notification.objects.create(
            user=self.user,
            message='Второе',
            notification_type='info'
        )
        
        notifications = Notification.objects.filter(user=self.user)
        
        # Уведомления должны быть отсортированы по убыванию даты
        self.assertGreater(notifications[0].timestamp, notifications[1].timestamp)