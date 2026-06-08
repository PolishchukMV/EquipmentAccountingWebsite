"""
Представления для приложения обслуживания.
"""

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Maintenance


class MaintenanceListView(ListView):
    """Список записей об обслуживании."""
    model = Maintenance
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'maintenances'


class MaintenanceDetailView(DetailView):
    """Детали записи об обслуживании."""
    model = Maintenance
    template_name = 'maintenance/maintenance_detail.html'
    context_object_name = 'maintenance'


class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание записи об обслуживании."""
    model = Maintenance
    fields = '__all__'
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance:maintenance_list')
    permission_required = 'maintenance.add_maintenance'


class MaintenanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование записи об обслуживании."""
    model = Maintenance
    fields = '__all__'
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance:maintenance_list')
    permission_required = 'maintenance.change_maintenance'


class MaintenanceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление записи об обслуживании."""
    model = Maintenance
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance:maintenance_list')
    permission_required = 'maintenance.delete_maintenance'


class MaintenanceCompleteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Отметка об завершении обслуживания."""
    model = Maintenance
    template_name = 'maintenance/maintenance_complete.html'
    
    def post(self, request, pk):
        maintenance = self.get_object()
        maintenance.status = 'completed'
        maintenance.save()
        messages.success(request, 'Обслуживание завершено')
        return redirect('maintenance:maintenance_detail', pk=pk)


class MaintenanceCalendarView(LoginRequiredMixin, ListView):
    """Календарь обслуживания."""
    model = Maintenance
    template_name = 'maintenance/maintenance_calendar.html'
    context_object_name = 'maintenances'


class UpcomingMaintenanceView(LoginRequiredMixin, ListView):
    """Ближайшее обслуживание."""
    model = Maintenance
    template_name = 'maintenance/upcoming_maintenance.html'
    context_object_name = 'maintenances'
