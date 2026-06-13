"""
Представления для приложения оборудования.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils.html import escape
from django.http import HttpResponse
from django.conf import settings
from .models import Equipment, Category, EquipmentLog, Assignment
from .forms import EquipmentForm
from .utils import generate_equipment_excel, export_equipment_to_xlsx, export_equipment_to_docx
from io import BytesIO


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
    form_class = EquipmentForm
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
        # Escape данных для защиты от XSS
        for field_name, field_value in form.cleaned_data.items():
            if isinstance(field_value, str):
                form.cleaned_data[field_name] = escape(field_value)
        
        response = super().form_valid(form)
        EquipmentLog.objects.create(
            equipment=self.object,
            action='created',
            user=self.request.user
        )
        messages.success(self.request, 'Оборудование успешно создано')
        return response

    def get_context_data(self, **kwargs):
        """Добавляет контекст для формы."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить оборудование'
        return context


class EquipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Редактирование записи об оборудовании.
    """
    
    model = Equipment
    form_class = EquipmentForm
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
        # Escape данных для защиты от XSS
        for field_name, field_value in form.cleaned_data.items():
            if isinstance(field_value, str):
                form.cleaned_data[field_name] = escape(field_value)
        
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

    def get_context_data(self, **kwargs):
        """Добавляет контекст для формы."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Редактировать оборудование'
        return context


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


class EquipmentFilterView(LoginRequiredMixin, ListView):
    """
    Фильтрация оборудования по статусу и категории.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_filter.html'
    context_object_name = 'equipment_list'
    paginate_by = 10
    permission_required = 'equipment.view_equipment'
    
    def get_context_data(self, **kwargs):
        """Добавляет списки категорий и подразделений в контекст."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        from apps.departments.models import Department
        context['departments'] = Department.objects.all()
        context['status_choices'] = Equipment.STATUS_CHOICES
        return context

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
        
        return queryset.order_by('-created_at')


class EquipmentStatusView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Изменение статуса оборудования.
    """
    
    model = Equipment
    template_name = 'equipment/equipment_status.html'
    permission_required = 'equipment.change_equipment'
    context_object_name = 'equipment'
    
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
            # Проверяем валидность статуса
            valid_statuses = [choice[0] for choice in Equipment.STATUS_CHOICES]
            if new_status not in valid_statuses:
                messages.error(request, 'Неверный статус')
                return redirect('equipment:equipment_detail', pk=pk)
            
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
        else:
            messages.error(request, 'Статус не указан')
        
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


def export_equipment_xlsx(request):
    """
    Экспорт всего оборудования в Excel.
    
    GET: /equipment/export/xlsx/
    """
    queryset = Equipment.objects.select_related(
        'category', 'department', 'responsible_person'
    ).all()
    return export_equipment_to_xlsx(queryset)


def export_equipment_docx(request):
    """
    Экспорт всего оборудования в Word.
    
    GET: /equipment/export/docx/
    """
    queryset = Equipment.objects.select_related(
        'category', 'department', 'responsible_person'
    ).all()
    # Для Word экспортируем как отдельную карточку каждого оборудования
    if not queryset.exists():
        messages.warning(request, 'Нет оборудования для экспорта')
        return redirect('equipment:equipment_list')
    
    # Экспортируем первое оборудование для примера
    return export_equipment_to_docx(queryset.first())


def export_equipment_detail(request, pk):
    """
    Экспорт конкретной единицы оборудования.
    
    GET: /equipment/<pk>/export/
    """
    equipment = get_object_or_404(Equipment, pk=pk)
    return export_equipment_to_docx(equipment)


def import_equipment(request):
    """
    Импорт оборудования из Excel/CSV.
    
    GET: страница загрузки файла
    POST: обработка файла
    """
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'Файл не выбран')
            return render(request, 'equipment/equipment_import.html')
        
        # Проверка расширения
        allowed_extensions = ['xlsx', 'xls', 'csv']
        ext = file.name.split('.')[-1].lower()
        if ext not in allowed_extensions:
            messages.error(request, f'Недопустимый формат. Разрешены: {", ".join(allowed_extensions)}')
            return render(request, 'equipment/equipment_import.html')
        
        try:
            # Простая обработка Excel файла
            import openpyxl
            wb = openpyxl.load_workbook(file)
            ws = wb.active
            
            imported_count = 0
            for row_num, row in enumerate(ws.iter_rows(values_only=True), start=2):
                if row_num == 2 and row[0] == 'Инвентарный номер':
                    # Пропускаем заголовок
                    continue
                if row[0]:  # Инвентарный номер
                    try:
                        Equipment.objects.create(
                            inventory_number=str(row[0]),
                            name=row[1] if len(row) > 1 else '',
                            category_id=row[2] if len(row) > 2 and row[2] else None,
                            serial_number=row[3] if len(row) > 3 else '',
                            manufacturer=row[4] if len(row) > 4 else '',
                            model=row[5] if len(row) > 5 else '',
                            status='in_stock',
                        )
                        imported_count += 1
                    except Exception as e:
                        messages.warning(request, f'Ошибка при обработке строки {row_num}: {str(e)}')
            
            messages.success(request, f'Импортировано записей: {imported_count}')
            return redirect('equipment:equipment_list')
            
        except Exception as e:
            messages.error(request, f'Ошибка при импорте: {str(e)}')
            return render(request, 'equipment/equipment_import.html')
    
    # GET запрос - показываем форму загрузки
    return render(request, 'equipment/equipment_import.html')
