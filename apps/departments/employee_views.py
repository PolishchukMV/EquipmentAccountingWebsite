"""
Представления для управления сотрудниками.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Employee, Department
from .employee_forms import EmployeeForm


class EmployeeListView(LoginRequiredMixin, ListView):
    """Список всех сотрудников."""
    
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    permission_required = 'departments.view_employee'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по подразделению
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        # Фильтр по статусу
        is_active = self.request.GET.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset.select_related('user', 'department').order_by('department', 'position')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    """Детали сотрудника."""
    
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'
    permission_required = 'departments.view_employee'


class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание нового сотрудника."""
    
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'
    permission_required = 'departments.add_employee'
    success_url = reverse_lazy('departments:employee_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Сотрудник успешно создан')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать сотрудника'
        return context


class EmployeeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование сотрудника."""
    
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'
    permission_required = 'departments.change_employee'
    success_url = reverse_lazy('departments:employee_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Сотрудник успешно обновлён')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать сотрудника'
        return context


class EmployeeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление сотрудника."""
    
    model = Employee
    template_name = 'employee/employee_confirm_delete.html'
    permission_required = 'departments.delete_employee'
    success_url = reverse_lazy('departments:employee_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, 'Сотрудник успешно удалён')
        return super().delete(request, *args, **kwargs)
