"""
URL-маршруты для приложения отчётов.
"""

from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportsDashboardView.as_view(), name='reports_dashboard'),
    path('inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    path('movement/', views.MovementReportView.as_view(), name='movement_report'),
    path('maintenance/', views.MaintenanceReportView.as_view(), name='maintenance_report'),
    path('status/', views.StatusReportView.as_view(), name='status_report'),
    path('financial/', views.FinancialReportView.as_view(), name='financial_report'),
    path('generate/', views.GenerateReportView.as_view(), name='generate_report'),
    path('history/', views.ReportHistoryView.as_view(), name='report_history'),
]