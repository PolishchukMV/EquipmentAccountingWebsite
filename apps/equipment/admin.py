"""
Админ-интерфейс для моделей оборудования.
"""

from django.contrib import admin
from .models import Category, Equipment, Assignment, EquipmentLog, Accessory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления категориями оборудования.
    """
    
    list_display = ['name', 'code', 'parent']
    list_filter = ['parent']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления оборудованием.
    
    Предоставляет полный контроль над записями оборудования с фильтрацией и поиском.
    """
    
    list_display = [
        'inventory_number', 'name', 'category', 'status', 
        'department', 'responsible_person', 'purchase_date'
    ]
    list_filter = ['status', 'category', 'department', 'purchase_date']
    search_fields = [
        'inventory_number', 'name', 'serial_number', 
        'manufacturer', 'model', 'location'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('inventory_number', 'name', 'category', 'status')
        }),
        ('Технические данные', {
            'fields': ('serial_number', 'manufacturer', 'model')
        }),
        ('Покупка и гарантия', {
            'fields': ('purchase_date', 'purchase_price', 'warranty_period')
        }),
        ('Расположение и ответственность', {
            'fields': ('department', 'responsible_person', 'location')
        }),
        ('Файлы', {
            'fields': ('photo', 'document')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления назначениями оборудования.
    """
    
    list_display = ['equipment', 'from_department', 'to_department', 'status', 'assignment_date']
    list_filter = ['status', 'assignment_date']
    search_fields = ['equipment__inventory_number', 'equipment__name']
    ordering = ['-assignment_date']


@admin.register(EquipmentLog)
class EquipmentLogAdmin(admin.ModelAdmin):
    """
    Админ-панель для просмотра журнала изменений оборудования.
    """
    
    list_display = ['equipment', 'action', 'user', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['equipment__inventory_number', 'equipment__name']
    ordering = ['-timestamp']
    
    readonly_fields = ['equipment', 'action', 'user', 'old_value', 'new_value', 'timestamp']


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления аксессуарами оборудования.
    """
    
    list_display = ['name', 'equipment', 'quantity']
    list_filter = ['equipment']
    search_fields = ['name', 'equipment__inventory_number']
    ordering = ['name']
