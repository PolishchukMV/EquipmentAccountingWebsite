"""
Представления для приложения отчётов.
"""

from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.db.models import Count, Sum
from apps.equipment.models import Equipment, Category, Assignment, EquipmentLog
from apps.maintenance.models import Maintenance
from apps.departments.models import Department
from apps.reports.models import Report
from .utils import generate_equipment_excel
from .docx_utils import generate_equipment_docx


class SuperUserRequiredMixin:
    """Миксин для разрешения доступа суперпользователям."""
    
    def has_permission(self):
        """Разрешаем доступ суперпользователям и пользователям с permission."""
        if self.request.user.is_superuser:
            return True
        # Проверяем наличие permission через PermissionRequiredMixin
        if hasattr(self, 'permission_required'):
            return self.request.user.has_perm(self.permission_required)
        return True


class ReportsDashboardView(LoginRequiredMixin, PermissionRequiredMixin, SuperUserRequiredMixin, TemplateView):
    """Дашборд отчётов."""
    template_name = 'reports/reports_dashboard.html'
    permission_required = 'reports.view_report'
    raise_exception = False
    
    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')


class InventoryReportView(LoginRequiredMixin, PermissionRequiredMixin, SuperUserRequiredMixin, TemplateView):
    """Отчёт по инвентаризации."""
    template_name = 'reports/inventory_report.html'
    permission_required = 'reports.view_report'
    raise_exception = False

    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')

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


class MovementReportView(LoginRequiredMixin, PermissionRequiredMixin, SuperUserRequiredMixin, TemplateView):
    """Отчёт по перемещениям."""
    template_name = 'reports/movement_report.html'
    permission_required = 'reports.view_report'
    raise_exception = False

    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movements'] = Assignment.objects.select_related(
            'equipment', 'from_department', 'to_department', 'user'
        ).all().order_by('-timestamp')
        return context


class MaintenanceReportView(LoginRequiredMixin, PermissionRequiredMixin, SuperUserRequiredMixin, TemplateView):
    """Отчёт по обслуживанию."""
    template_name = 'reports/maintenance_report.html'
    permission_required = 'reports.view_report'
    raise_exception = False

    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenances'] = Maintenance.objects.select_related(
            'equipment'
        ).all().order_by('-scheduled_date')
        context['total_cost'] = Maintenance.objects.aggregate(
            total=Sum('cost')
        )['total'] or 0
        return context


class StatusReportView(LoginRequiredMixin, PermissionRequiredMixin, SuperUserRequiredMixin, TemplateView):
    """Отчёт по статусам оборудования."""
    template_name = 'reports/status_report.html'
    permission_required = 'reports.view_report'
    raise_exception = False

    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_stats'] = Equipment.objects.values(
            'status'
        ).annotate(
            count=Count('id')
        ).order_by('status')
        return context


class FinancialReportView(LoginRequiredMixin, PermissionRequiredMixin, SuperUserRequiredMixin, TemplateView):
    """Финансовый отчёт."""
    template_name = 'reports/financial_report.html'
    permission_required = 'reports.view_report'
    raise_exception = False

    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')

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


class ReportHistoryView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    """История отчётов."""
    template_name = 'reports/report_history.html'
    context_object_name = 'reports'
    raise_exception = False

    def handle_no_permission(self):
        """Перенаправляем на главную при отсутствии прав."""
        return redirect(settings.LOGIN_URL if not self.request.user.is_authenticated else '/')
    
    def get_queryset(self):
        # Суперпользователи видят все отчёты, другие только свои
        if self.request.user.is_superuser:
            return Report.objects.all().order_by('-generated_at')
        return Report.objects.filter(
            generated_by=self.request.user
        ).order_by('-generated_at')
