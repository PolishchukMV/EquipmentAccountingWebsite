"""
Формы для приложения аутентификации и пользователей.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя.
    
    Расширяет стандартную форму UserCreationForm, добавляя поля email и role.
    """
    
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        label='Роль',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Подтвердите пароль'
            }),
        }
    
    def clean_email(self):
        """
        Проверяет уникальность email.
        
        Returns:
            str: Очищенный email
            
        Raises:
            ValidationError: Если email уже зарегистрирован
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма редактирования профиля пользователя.
    
    Позволяет обновлять личные данные и настройки профиля.
    """
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar', 'department')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 000-00-00'
            }),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_phone(self):
        """
        Проверяет формат номера телефона.
        
        Returns:
            str: Очищенный номер телефона
        """
        phone = self.cleaned_data.get('phone')
        # Простая валидация: номер должен содержать только цифры, +, -, (), пробелы
        if phone and not all(c in '+-() 0123456789' for c in phone):
            raise forms.ValidationError('Неверный формат номера телефона')
        return phone
