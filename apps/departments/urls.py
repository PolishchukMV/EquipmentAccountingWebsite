"""
URL-маршруты для приложения подразделений.
"""

from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department_list'),
    path('<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('<int:pk>/employees/', views.DepartmentEmployeesView.as_view(), name='department_employees'),
    path('<int:pk>/equipment/', views.DepartmentEquipmentView.as_view(), name='department_equipment'),
]