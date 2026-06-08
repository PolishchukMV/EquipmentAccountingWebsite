"""
URL-маршруты для приложения оборудования.
"""

from django.urls import path
from . import views

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
    
    # Категории
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Журнал
    path('<int:pk>/history/', views.EquipmentHistoryView.as_view(), name='equipment_history'),
]