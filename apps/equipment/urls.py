"""
URL-маршруты для приложения оборудования.
"""

from django.urls import path
from . import views
from .assignment_views import (
    AssignmentListView,
    AssignmentDetailView,
    AssignmentCreateView,
    AssignmentUpdateView,
    AssignmentDeleteView,
    AssignmentReturnView,
    MyAssignmentsView,
)

app_name = 'equipment'

urlpatterns = [
    # Главная страница
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    
    # Поиск и фильтрация
    path('search/', views.EquipmentSearchView.as_view(), name='equipment_search'),
    path('filter/', views.EquipmentFilterView.as_view(), name='equipment_filter'),
    
    # Статусы
    path('<int:pk>/status/', views.EquipmentStatusView.as_view(), name='equipment_status'),
    
    # Экспорт
    path('export/xlsx/', views.export_equipment_xlsx, name='export_xlsx'),
    path('export/docx/', views.export_equipment_docx, name='export_docx'),
    path('<int:pk>/export/', views.export_equipment_detail, name='export_detail'),
    
    # Импорт
    path('import/', views.import_equipment, name='import_equipment'),
    
    # Категории
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Журнал
    path('<int:pk>/history/', views.EquipmentHistoryView.as_view(), name='equipment_history'),
    
    # Назначения (Assignment)
    path('assignments/', AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/<int:pk>/update/', AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('assignments/<int:pk>/return/', AssignmentReturnView.as_view(), name='assignment_return'),
    path('my-assignments/', MyAssignmentsView.as_view(), name='my_assignments'),
]