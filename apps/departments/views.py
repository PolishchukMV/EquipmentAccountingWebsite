"""
Представления для приложения подразделений.
"""

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Department, Employee


class DepartmentListView(ListView):
    """Список подразделений."""
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'


class DepartmentDetailView(DetailView):
    """Детали подразделения."""
    model = Department
    template_name = 'departments/department_detail.html'
    context_object_name = 'department'


class DepartmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание подразделения."""
    model = Department
    fields = '__all__'
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')
    permission_required = 'departments.add_department'


class DepartmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование подразделения."""
    model = Department
    fields = '__all__'
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('departments:department_list')
    permission_required = 'departments.change_department'


class DepartmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление подразделения."""
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('departments:department_list')
    permission_required = 'departments.delete_department'


class DepartmentEmployeesView(DetailView):
    """Список сотрудников подразделения."""
    model = Department
    template_name = 'departments/department_employees.html'
    context_object_name = 'department'


class DepartmentEquipmentView(DetailView):
    """Оборудование подразделения."""
    model = Department
    template_name = 'departments/department_equipment.html'
    context_object_name = 'department'
