"""
Админ-интерфейс для моделей обслуживания.
"""

from django.contrib import admin
from .models import Maintenance


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления обслуживанием оборудования.
    
    Предоставляет контроль над записями обслуживания с фильтрацией по статусу и типу.
    """
    
    list_display = [
        'equipment', 'maintenance_type', 'status', 
        'scheduled_date', 'completed_date', 'cost'
    ]
    list_filter = ['maintenance_type', 'status', 'scheduled_date']
    search_fields = ['equipment__inventory_number', 'equipment__name', 'description']
    ordering = ['-scheduled_date']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('equipment', 'maintenance_type', 'status')
        }),
        ('Даты', {
            'fields': ('scheduled_date', 'completed_date')
        }),
        ('Описание работ', {
            'fields': ('description', 'cost', 'contractor', 'technician')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'document', 'created_at')
        }),
    )
    
    readonly_fields = ['created_at']
