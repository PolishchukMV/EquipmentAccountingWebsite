"""
Админ-интерфейс для моделей отчётов.
"""

from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления отчётами.
    
    Позволяет просматривать историю сгенерированных отчётов.
    """
    
    list_display = ['name', 'report_type', 'format', 'generated_by', 'generated_at']
    list_filter = ['report_type', 'format', 'generated_at']
    search_fields = ['name', 'generated_by__username']
    ordering = ['-generated_at']
    
    readonly_fields = ['name', 'report_type', 'format', 'parameters', 'file', 'generated_by', 'generated_at']
