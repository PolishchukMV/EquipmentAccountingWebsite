"""
Модели отчётов для системы учёта оборудования.
"""

from django.db import models


class Report(models.Model):
    """
    Модель отчёта системы.
    
    Хранит информацию о сгенерированных отчётах.
    
    Поля:
        name: Название отчёта
        report_type: Тип отчёта
        format: Формат экспорта
        parameters: Параметры генерации (JSON)
        file: Сгенерированный файл
        generated_by: Пользователь, создавший отчёт
        generated_at: Дата генерации
    """
    
    TYPE_CHOICES = [
        ('inventory', 'Инвентаризация'),
        ('movement', 'Перемещения'),
        ('maintenance', 'Обслуживание'),
        ('status', 'Статус оборудования'),
        ('financial', 'Финансовый'),
    ]
    
    FORMAT_CHOICES = [
        ('xlsx', 'Excel'),
        ('docx', 'Word'),
        ('pdf', 'PDF'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    report_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Тип отчёта'
    )
    format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default='xlsx',
        verbose_name='Формат'
    )
    parameters = models.JSONField(
        default=dict,
        verbose_name='Параметры'
    )
    file = models.FileField(
        upload_to='reports/',
        verbose_name='Файл'
    )
    generated_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создатель'
    )
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата генерации'
    )
    
    class Meta:
        db_table = 'reports_report'
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['-generated_at']
    
    def __str__(self):
        """Возвращает название и тип отчёта."""
        return f'{self.name} ({self.get_report_type_display()})'
