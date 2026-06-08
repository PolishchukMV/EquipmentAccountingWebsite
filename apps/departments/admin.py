"""
Админ-интерфейс для моделей подразделений.
"""

from django.contrib import admin
from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления подразделениями.
    """
    
    list_display = ['name', 'code', 'parent', 'head', 'created_at']
    list_filter = ['parent', 'head']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления сотрудниками.
    """
    
    list_display = ['user', 'department', 'position', 'employee_id', 'hire_date', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'employee_id']
    ordering = ['department', 'position']
