"""
Представления для приложения отчётов.
"""

from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Sum
from apps.equipment.models import Equipment, Category, Assignment, EquipmentLog
from apps.maintenance.models import Maintenance
from apps.departments.models import Department
from apps.reports.models import Report
from .utils import generate_equipment_excel
from .docx_utils import generate_equipment_docx


class ReportsDashboardView(TemplateView):
    """Дашборд отчётов."""
    template_name = 'reports/reports_dashboard.html'


class InventoryReportView(LoginRequiredMixin, TemplateView):
    """Отчёт по инвентаризации."""
    template_name = 'reports/inventory_report.html'

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('format')
        equipment = Equipment.objects.select_related(
            'category', 'department', 'responsible_person'
        ).all().order_by('inventory_number')

        if export_format == 'xlsx':
            excel_file = generate_equipment_excel(equipment)
            response = HttpResponse(
                excel_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=equipment_report.xlsx'
            return response
        
        elif export_format == 'docx':
            docx_file = generate_equipment_docx(equipment)
            response = HttpResponse(
                docx_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename=equipment_report.docx'
            return response
        
        context = self.get_context_data(**kwargs)
        context['equipment_list'] = equipment
        return self.render_to_response(context)


class MovementReportView(LoginRequiredMixin, TemplateView):
    """Отчёт по перемещениям."""
    template_name = 'reports/movement_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movements'] = Assignment.objects.select_related(
            'equipment', 'from_department', 'to_department', 'user'
        ).all().order_by('-timestamp')
        return context


class MaintenanceReportView(LoginRequiredMixin, TemplateView):
    """Отчёт по обслуживанию."""
    template_name = 'reports/maintenance_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenances'] = Maintenance.objects.select_related(
            'equipment'
        ).all().order_by('-start_date')
        context['total_cost'] = Maintenance.objects.aggregate(
            total=Sum('cost')
        )['total'] or 0
        return context


class StatusReportView(LoginRequiredMixin, TemplateView):
    """Отчёт по статусам оборудования."""
    template_name = 'reports/status_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_stats'] = Equipment.objects.values(
            'status'
        ).annotate(
            count=Count('id')
        ).order_by('status')
        return context


class FinancialReportView(LoginRequiredMixin, TemplateView):
    """Финансовый отчёт."""
    template_name = 'reports/financial_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment_total'] = Equipment.objects.aggregate(
            total=Sum('purchase_price')
        )['total'] or 0
        context['maintenance_total'] = Maintenance.objects.aggregate(
            total=Sum('cost')
        )['total'] or 0
        context['grand_total'] = context['equipment_total'] + context['maintenance_total']
        return context


class GenerateReportView(TemplateView):
    """Генерация отчёта."""
    template_name = 'reports/generate_report.html'


class ReportHistoryView(LoginRequiredMixin, ListView):
    """История отчётов."""
    template_name = 'reports/report_history.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
