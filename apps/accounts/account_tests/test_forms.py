"""
Тесты для форм приложения accounts.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.forms import UserRegistrationForm, UserProfileForm


UserModel = get_user_model()


class UserRegistrationFormTest(TestCase):
    """Тесты для формы регистрации пользователя."""
    
    def test_valid_registration_form(self):
        """Тест валидной формы регистрации."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        
        self.assertTrue(form.is_valid())
    
    def test_passwords_mismatch(self):
        """Тест несовпадения паролей."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'DifferentPass123!'
        }
        form = UserRegistrationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_weak_password(self):
        """Тест слабого пароля."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': '123',
            'password2': '123'
        }
        form = UserRegistrationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
    
    def test_missing_username(self):
        """Тест отсутствия имени пользователя."""
        form_data = {
            'username': '',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_invalid_email(self):
        """Тест невалидного email."""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!'
        }
        form = UserRegistrationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class UserProfileFormTest(TestCase):
    """Тесты для формы профиля пользователя."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Иванов',
            phone='+79001234567'
        )
    
    def test_valid_profile_form(self):
        """Тест валидной формы профиля."""
        form_data = {
            'first_name': 'Петр',
            'last_name': 'Петров',
            'email': 'newemail@example.com',
            'phone': '+79009876543'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        
        self.assertTrue(form.is_valid())
    
    def test_update_profile(self):
        """Тест обновления профиля."""
        form_data = {
            'first_name': 'Петр',
            'last_name': 'Петров',
            'email': 'newemail@example.com',
            'phone': '+79009876543'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        
        if form.is_valid():
            user = form.save()
            self.assertEqual(user.first_name, 'Петр')
            self.assertEqual(user.last_name, 'Петров')
            self.assertEqual(user.phone, '+79009876543')
    
    def test_empty_phone(self):
        """Тест пустого телефона."""
        form_data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'test@example.com',
            'phone': ''
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        
        self.assertTrue(form.is_valid())