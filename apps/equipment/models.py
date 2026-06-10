"""
Модели оборудования для системы учёта.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """
    Категория оборудования.
    
    Поддерживает иерархическую структуру категорий.
    
    Поля:
        name: Название категории
        code: Уникальный код
        parent: Родительская категория
        description: Описание
    """
    
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Код'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    class Meta:
        db_table = 'equipment_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        """Возвращает название категории."""
        return self.name


class Equipment(models.Model):
    """
    Основная модель оборудования.
    
    Хранит информацию о каждой единице оборудования компании.
    
    Поля:
        inventory_number: Инвентарный номер (уникальный)
        name: Наименование
        category: Категория оборудования
        serial_number: Серийный номер
        manufacturer: Производитель
        model: Модель
        purchase_date: Дата покупки
        purchase_price: Цена покупки
        warranty_period: Гарантийный срок (месяцев)
        status: Текущий статус
        department: Подразделение
        responsible_person: Ответственное лицо
        location: Местоположение
        notes: Примечания
        photo: Фотография
        document: Документ
        created_at: Дата создания
        updated_at: Дата обновления
    """
    
    STATUS_CHOICES = [
        ('in_stock', 'На складе'),
        ('in_use', 'В эксплуатации'),
        ('in_repair', 'В ремонте'),
        ('out_of_order', 'Неисправно'),
    ]
    
    inventory_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Инвентарный номер'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Серийный номер'
    )
    manufacturer = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Производитель'
    )
    model = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Модель'
    )
    purchase_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата покупки'
    )
    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Цена покупки'
    )
    warranty_period = models.IntegerField(
        null=True,
        blank=True,
        help_text='Месяцев',
        verbose_name='Гарантийный срок',
        validators=[
            MinValueValidator(0, message='Гарантийный срок не может быть отрицательным'),
            MaxValueValidator(1200, message='Гарантийный срок слишком большой'),
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Статус'
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Подразделение'
    )
    responsible_person = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Ответственное лицо'
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Местоположение'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Примечания'
    )
    photo = models.ImageField(
        upload_to='equipment/photos/',
        null=True,
        blank=True,
        verbose_name='Фотография'
    )
    document = models.FileField(
        upload_to='equipment/documents/',
        null=True,
        blank=True,
        verbose_name='Документ'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        db_table = 'equipment_equipment'
        verbose_name = 'Единица оборудования'
        verbose_name_plural = 'Оборудование'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['inventory_number']),
            models.Index(fields=['status']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        """Возвращает инвентарный номер и название."""
        return f'{self.inventory_number} - {self.name}'
    
    def get_status_display_ru(self):
        """Возвращает отображение статуса на русском языке."""
        return self.get_status_display()
    
    def is_available(self):
        """Проверяет, доступно ли оборудование."""
        return self.status == 'available'
    
    def warranty_expired(self):
        """
        Проверяет, истёк ли гарантийный срок.
        
        Returns:
            bool: True если гарантия истекла
        """
        if not self.purchase_date or not self.warranty_period:
            return False
        from datetime import date, timedelta
        warranty_end = self.purchase_date + timedelta(days=self.warranty_period * 30)
        return date.today() > warranty_end


class Assignment(models.Model):
    """
    Модель назначения/перемещения оборудования.
    
    Отслеживает историю передачи оборудования между подразделениями и сотрудниками.
    
    Поля:
        equipment: Оборудование
        from_department: Исходное подразделение
        to_department: Целевое подразделение
        from_person: Отдающий сотрудник
        to_person: Принимающий сотрудник
        assignment_date: Дата назначения
        return_date: Дата возврата
        reason: Причина
        status: Статус
        document: Документ
        created_by: Создатель записи
    """
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    from_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='from_assignments',
        verbose_name='Откуда'
    )
    to_department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='to_assignments',
        verbose_name='Куда'
    )
    from_person = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='from_assignments',
        verbose_name='Отдающий'
    )
    to_person = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='to_assignments',
        verbose_name='Принимающий'
    )
    assignment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата назначения'
    )
    return_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата возврата'
    )
    reason = models.TextField(
        verbose_name='Причина'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Активно'),
            ('returned', 'Возвращено'),
            ('cancelled', 'Отменено'),
        ],
        default='active',
        verbose_name='Статус'
    )
    document = models.FileField(
        upload_to='assignments/',
        null=True,
        blank=True,
        verbose_name='Документ'
    )
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Создатель'
    )
    
    class Meta:
        db_table = 'equipment_assignment'
        verbose_name = 'Назначение оборудования'
        verbose_name_plural = 'Назначения оборудования'
        ordering = ['-assignment_date']
    
    def __str__(self):
        """Возвращает информацию о назначении."""
        return f'{self.equipment} -> {self.to_department or self.to_person}'


class EquipmentLog(models.Model):
    """
    Журнал изменений оборудования.
    
    Отслеживает все изменения в записях оборудования.
    
    Поля:
        equipment: Оборудование
        action: Тип действия
        user: Пользователь, выполнивший действие
        old_value: Старое значение
        new_value: Новое значение
        timestamp: Время изменения
    """
    
    ACTION_CHOICES = [
        ('created', 'Создано'),
        ('updated', 'Обновлено'),
        ('status_changed', 'Статус изменён'),
        ('assigned', 'Назначено'),
        ('returned', 'Возвращено'),
        ('deleted', 'Удалено'),
    ]
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name='Оборудование'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Действие'
    )
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Пользователь'
    )
    old_value = models.TextField(
        blank=True,
        verbose_name='Старое значение'
    )
    new_value = models.TextField(
        blank=True,
        verbose_name='Новое значение'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время изменения'
    )
    
    class Meta:
        db_table = 'equipment_equipmentlog'
        verbose_name = 'Журнал изменений'
        verbose_name_plural = 'Журнал изменений'
        ordering = ['-timestamp']
    
    def __str__(self):
        """Возвращает описание изменения."""
        return f'{self.action}: {self.equipment} ({self.timestamp})'


class Accessory(models.Model):
    """
    Аксессуар/комплектующее для оборудования.
    
    Поля:
        equipment: Оборудование
        name: Название аксессуара
        quantity: Количество
        serial_number: Серийный номер
        notes: Примечания
    """
    
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='accessories',
        verbose_name='Оборудование'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название'
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name='Количество'
    )
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Серийный номер'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Примечания'
    )
    
    class Meta:
        db_table = 'equipment_accessory'
        verbose_name = 'Аксессуар'
        verbose_name_plural = 'Аксессуары'
        ordering = ['name']
    
    def __str__(self):
        """Возвращает название аксессуара и количество."""
        return f'{self.name} ({self.quantity} шт.)'
