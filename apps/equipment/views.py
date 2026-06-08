"""
Представления для приложения оборудования.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Equipment, Category, EquipmentLog


class EquipmentListView(ListView):
    """
    Просмотр списка всего оборудования.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment_list'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Возвращает все записи оборудования с сортировкой по дате создания.
        
        Returns:
            QuerySet: Отфильтрованный и отсортированный набор записей
        """
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')


class EquipmentDetailView(DetailView):
    """
    Просмотр деталей конкретной единицы оборудования.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'


class EquipmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Создание новой записи об оборудовании.
    """
    
    model = Equipment
    fields = '__all__'
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:equipment_list')
    permission_required = 'equipment.add_equipment'
    
    def form_valid(self, form):
        """
        Вызывается при успешной валидации формы.
        Создаёт запись в журнале изменений.
        
        Args:
            form: Форма создания оборудования
            
        Returns:
            redirect: Перенаправление на список оборудования
        """
        response = super().form_valid(form)
        EquipmentLog.objects.create(
            equipment=self.object,
            action='created',
            user=self.request.user
        )
        messages.success(self.request, 'Оборудование успешно создано')
        return response


class EquipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Редактирование записи об оборудовании.
    """
    
    model = Equipment
    fields = '__all__'
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:equipment_list')
    permission_required = 'equipment.change_equipment'
    
    def form_valid(self, form):
        """
        Вызывается при успешной валидации формы.
        Создаёт запись в журнале изменений.
        
        Args:
            form: Форма редактирования оборудования
            
        Returns:
            redirect: Перенаправление на список оборудования
        """
        response = super().form_valid(form)
        EquipmentLog.objects.create(
            equipment=self.object,
            action='updated',
            user=self.request.user,
            old_value=str(form.initial),
            new_value=str(form.cleaned_data)
        )
        messages.success(self.request, 'Оборудование успешно обновлено')
        return response


class EquipmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Удаление записи об оборудовании.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment:equipment_list')
    permission_required = 'equipment.delete_equipment'
    
    def delete(self, request, *args, **kwargs):
        """
        Вызывается при удалении объекта.
        Создаёт запись в журнале изменений.
        
        Args:
            request: Объект запроса
            
        Returns:
            redirect: Перенаправление на список оборудования
        """
        self.object = self.get_object()
        EquipmentLog.objects.create(
            equipment=self.object,
            action='deleted',
            user=request.user
        )
        messages.success(request, 'Оборудование успешно удалено')
        return super().delete(request, *args, **kwargs)


class EquipmentSearchView(ListView):
    """
    Поиск оборудования по различным полям.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_search.html'
    context_object_name = 'equipment_list'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Фильтрует оборудование по поисковому запросу.
        
        Returns:
            QuerySet: Отфильтрованный набор записей
        """
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(inventory_number__icontains=query) |
                Q(name__icontains=query) |
                Q(serial_number__icontains=query) |
                Q(manufacturer__icontains=query) |
                Q(model__icontains=query)
            )
        return queryset


class EquipmentFilterView(ListView):
    """
    Фильтрация оборудования по статусу и категории.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_filter.html'
    context_object_name = 'equipment_list'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Фильтрует оборудование по переданным параметрам.
        
        Returns:
            QuerySet: Отфильтрованный набор записей
        """
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        category = self.request.GET.get('category')
        department = self.request.GET.get('department')
        
        if status:
            queryset = queryset.filter(status=status)
        if category:
            queryset = queryset.filter(category_id=category)
        if department:
            queryset = queryset.filter(department_id=department)
        
        return queryset


class EquipmentStatusView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Изменение статуса оборудования.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_status.html'
    permission_required = 'equipment.change_equipment'
    
    def post(self, request, pk):
        """
        Обрабатывает POST запрос на изменение статуса.
        
        Args:
            request: Объект запроса
            pk: ID оборудования
            
        Returns:
            redirect: Перенаправление на детали оборудования
        """
        equipment = get_object_or_404(Equipment, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status:
            old_status = equipment.status
            equipment.status = new_status
            equipment.save()
            
            EquipmentLog.objects.create(
                equipment=equipment,
                action='status_changed',
                user=request.user,
                old_value=old_status,
                new_value=new_status
            )
            messages.success(request, f'Статус изменён на {equipment.get_status_display()}')
        
        return redirect('equipment:equipment_detail', pk=pk)


class EquipmentHistoryView(DetailView):
    """
    Просмотр истории изменений оборудования.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_history.html'
    context_object_name = 'equipment'
    
    def get_context_data(self, **kwargs):
        """
        Добавляет историю изменений в контекст шаблона.
        
        Returns:
            dict: Контекст с историей изменений
        """
        context = super().get_context_data(**kwargs)
        context['history'] = EquipmentLog.objects.filter(
            equipment=self.object
        ).order_by('-timestamp')
        return context


class CategoryListView(ListView):
    """
    Просмотр списка категорий оборудования.
    """
    
    model = Category
    template_name = 'equipment/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    """
    Просмотр деталей категории оборудования.
    """
    
    model = Category
    template_name = 'equipment/category_detail.html'
    context_object_name = 'category'


def bad_request(request, exception):
    """Обработчик ошибки 400."""
    return render(request, 'errors/400.html', status=400)


def forbidden(request, exception):
    """Обработчик ошибки 403."""
    return render(request, 'errors/403.html', status=403)


def not_found(request, exception):
    """Обработчик ошибки 404."""
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    """Обработчик ошибки 500."""
    return render(request, 'errors/500.html', status=500)
