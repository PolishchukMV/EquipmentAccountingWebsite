"""
Представления для приложения отчётов.
"""

from django.shortcuts import render
from django.views.generic import ListView, TemplateView


class ReportsDashboardView(TemplateView):
    """Дашборд отчётов."""
    template_name = 'reports/reports_dashboard.html'


class InventoryReportView(TemplateView):
    """Отчёт по инвентаризации."""
    template_name = 'reports/inventory_report.html'


class MovementReportView(TemplateView):
    """Отчёт по перемещениям."""
    template_name = 'reports/movement_report.html'


class MaintenanceReportView(TemplateView):
    """Отчёт по обслуживанию."""
    template_name = 'reports/maintenance_report.html'


class StatusReportView(TemplateView):
    """Отчёт по статусам оборудования."""
    template_name = 'reports/status_report.html'


class FinancialReportView(TemplateView):
    """Финансовый отчёт."""
    template_name = 'reports/financial_report.html'


class GenerateReportView(TemplateView):
    """Генерация отчёта."""
    template_name = 'reports/generate_report.html'


class ReportHistoryView(ListView):
    """История отчётов."""
    template_name = 'reports/report_history.html'
