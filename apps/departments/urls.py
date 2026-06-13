"""
URL-маршруты для приложения подразделений.
"""

from django.urls import path
from . import views
from .employee_views import (
    EmployeeListView,
    EmployeeDetailView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
)

app_name = 'departments'

urlpatterns = [
    # Подразделения
    path('', views.DepartmentListView.as_view(), name='department_list'),
    path('<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('<int:pk>/employees/', views.DepartmentEmployeesView.as_view(), name='department_employees'),
    path('<int:pk>/equipment/', views.DepartmentEquipmentView.as_view(), name='department_equipment'),
    
    # Сотрудники
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
]