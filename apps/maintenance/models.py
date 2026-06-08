"""
Модели обслуживания и ремонта оборудования.
"""

from django.db import models


class Maintenance(models.Model):
    """
    Модель записи об обслуживании или ремонте оборудования.
    
    Отслеживает плановое и внеплановое обслуживание оборудования.
    
    Поля:
        equipment: Обслуживаемое оборудование
        maintenance_type: Тип обслуживания
        status: Статус выполнения
        scheduled_date: Запланированная дата
        completed_date: Дата выполнения
        description: Описание работ
        cost: Стоимость работ
        contractor: Исполнитель работ
        technician: Технический специалист
        notes: Примечания
        document: Документ
        created_at: Дата создания записи
    """
    
    TYPE_CHOICES = [
        ('planned', 'Плановое'),
        ('repair', 'Ремонт'),
        ('inspection', 'Инспекция'),
        ('upgrade', 'Модернизация'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    equipment = models.ForeignKey(
        'equipment.Equipment',
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    maintenance_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Тип обслуживания'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name='Статус'
    )
    scheduled_date = models.DateField(
        verbose_name='Запланированная дата'
    )
    completed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата выполнения'
    )
    description = models.TextField(
        verbose_name='Описание работ'
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Стоимость'
    )
    contractor = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Исполнитель'
    )
    technician = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Технический специалист'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Примечания'
    )
    document = models.FileField(
        upload_to='maintenance/',
        null=True,
        blank=True,
        verbose_name='Документ'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        db_table = 'maintenance_maintenance'
        verbose_name = 'Обслуживание'
        verbose_name_plural = 'Обслуживание'
        ordering = ['-scheduled_date']
    
    def __str__(self):
        """Возвращает информацию об обслуживании."""
        return f'{self.equipment} - {self.get_maintenance_type_display()}'
    
    def is_overdue(self):
        """
        Проверяет, просрочено ли обслуживание.
        
        Returns:
            bool: True если обслуживание просрочено
        """
        from datetime import date
        return self.status != 'completed' and self.scheduled_date < date.today()
    
    def days_until_due(self):
        """
        Возвращает количество дней до запланированной даты.
        
        Returns:
            int: Количество дней (отрицательное если просрочено)
        """
        from datetime import date
        delta = self.scheduled_date - date.today()
        return delta.days
