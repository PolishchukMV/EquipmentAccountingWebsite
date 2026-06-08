"""
Тесты для views приложения accounts.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.departments.models import Department


UserModel = get_user_model()


class LoginViewTest(TestCase):
    """Тесты для страницы входа."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.login_url = reverse('accounts:login')
    
    def test_login_page_loads(self):
        """Тест загрузки страницы входа."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_success(self):
        """Тест успешного входа."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertRedirects(response, reverse('equipment:equipment_list'))
    
    def test_login_failure_wrong_password(self):
        """Тест неудачного входа с неправильным паролем."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверное имя пользователя или пароль')
    
    def test_login_failure_nonexistent_user(self):
        """Тест неудачного входа с несуществующим пользователем."""
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': 'password'
        })
        
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    """Тесты для страницы профиля."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile_url = reverse('accounts:profile')
    
    def test_profile_requires_login(self):
        """Тест, что профиль требует авторизации."""
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.profile_url}')
    
    def test_profile_page_loads(self):
        """Тест загрузки страницы профиля."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
    
    def test_profile_shows_user_info(self):
        """Тест отображения информации о пользователе."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'test@example.com')