"""
Админ-интерфейс для моделей пользователей и уведомлений.
"""

from django.contrib import admin
from .models import CustomUser, Notification


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления пользователями.
    
    Отображает основные поля пользователей и позволяет фильтровать по роли и подразделению.
    """
    
    list_display = ['username', 'email', 'role', 'department', 'phone', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'department']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Права доступа', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Дополнительно', {'fields': ('department', 'avatar', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления уведомлениями.
    """
    
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['title', 'message', 'user__username']
    ordering = ['-created_at']
    
    readonly_fields = ['created_at']
