"""
Админ-интерфейс для моделей обратной связи.
"""

from django.contrib import admin
from .models import FeedbackMessage


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления сообщениями обратной связи.
    
    Позволяет администраторам просматривать и обрабатывать обращения пользователей.
    """
    
    list_display = ['subject', 'author', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['subject', 'message', 'author__username', 'email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('subject', 'author', 'email', 'status')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Ответ', {
            'fields': ('response', 'responded_by', 'responded_at')
        }),
        ('Дополнительно', {
            'fields': ('created_at',)
        }),
    )
    
    readonly_fields = ['created_at', 'responded_at']
