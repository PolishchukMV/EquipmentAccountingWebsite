"""
Представления для назначений оборудования.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, EquipmentLog, Equipment
from .assignment_forms import AssignmentForm, AssignmentReturnForm


class AssignmentListView(LoginRequiredMixin, ListView):
    """Список всех назначений оборудования."""
    
    model = Assignment
    template_name = 'assignment/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 10
    permission_required = 'equipment.view_assignment'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Фильтр по оборудованию
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        
        return queryset.select_related(
            'equipment', 'from_department', 'to_department',
            'from_person', 'to_person', 'created_by'
        ).order_by('-assignment_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Assignment.STATUS_CHOICES
        context['equipment_list'] = Equipment.objects.all()
        return context


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    """Детали назначения оборудования."""
    
    model = Assignment
    template_name = 'assignment/assignment_detail.html'
    context_object_name = 'assignment'
    permission_required = 'equipment.view_assignment'


class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание нового назначения оборудования."""
    
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/assignment_form.html'
    permission_required = 'equipment.add_assignment'
    
    def get_success_url(self):
        return reverse_lazy('equipment:assignment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Автоматически меняем статус оборудования
        equipment = form.instance.equipment
        old_status = equipment.status
        equipment.status = 'in_use'
        equipment.save()
        
        response = super().form_valid(form)
        
        # Логируем назначение
        EquipmentLog.objects.create(
            equipment=equipment,
            action='assigned',
            user=self.request.user,
            old_value=old_status,
            new_value='in_use'
        )
        
        messages.success(self.request, 'Назначение успешно создано')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создать назначение'
        return context


class AssignmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование назначения оборудования."""
    
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/assignment_form.html'
    permission_required = 'equipment.change_assignment'
    
    def get_success_url(self):
        return reverse_lazy('equipment:assignment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Назначение успешно обновлено')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать назначение'
        return context


class AssignmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление назначения оборудования."""
    
    model = Assignment
    template_name = 'assignment/assignment_confirm_delete.html'
    permission_required = 'equipment.delete_assignment'
    success_url = reverse_lazy('equipment:assignment_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        equipment = self.object.equipment
        
        # Возвращаем статус оборудования если назначение отменяется
        if self.object.status == 'active':
            equipment.status = 'available'
            equipment.save()
            
            EquipmentLog.objects.create(
                equipment=equipment,
                action='returned',
                user=request.user,
                old_value='in_use',
                new_value='available'
            )
        
        messages.success(request, 'Назначение успешно удалено')
        return super().delete(request, *args, **kwargs)


class AssignmentReturnView(LoginRequiredMixin, DetailView):
    """Возврат оборудования."""
    
    model = Assignment
    template_name = 'assignment/assignment_return.html'
    context_object_name = 'assignment'
    
    def post(self, request, pk):
        assignment = get_object_or_404(Assignment, pk=pk)
        
        if assignment.status != 'active':
            messages.error(request, 'Это назначение уже завершено')
            return redirect('equipment:assignment_detail', pk=pk)
        
        form = AssignmentReturnForm(request.POST)
        if form.is_valid():
            # Меняем статус назначения
            assignment.status = 'returned'
            assignment.return_date = timezone.now()
            assignment.save()
            
            # Возвращаем статус оборудования
            equipment = assignment.equipment
            equipment.status = 'available'
            equipment.save()
            
            # Логируем возврат
            EquipmentLog.objects.create(
                equipment=equipment,
                action='returned',
                user=request.user,
                old_value='in_use',
                new_value='available'
            )
            
            messages.success(request, 'Оборудование успешно возвращено')
            return redirect('equipment:assignment_detail', pk=pk)
        
        messages.error(request, 'Ошибка при возврате оборудования')
        return redirect('equipment:assignment_detail', pk=pk)


class MyAssignmentsView(LoginRequiredMixin, ListView):
    """Мои назначения (оборудование на моей ответственности)."""
    
    model = Assignment
    template_name = 'assignment/my_assignments.html'
    context_object_name = 'assignments'
    paginate_by = 10
    
    def get_queryset(self):
        return Assignment.objects.filter(
            to_person=self.request.user,
            status='active'
        ).select_related('equipment', 'to_department').order_by('-assignment_date')
