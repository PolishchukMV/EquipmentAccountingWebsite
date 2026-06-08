"""
Модели подразделений компании для системы учёта оборудования.
"""

from django.db import models


class Department(models.Model):
    """
    Модель подразделения компании.
    
    Поддерживает иерархическую структуру (родительское/дочерние подразделения).
    
    Поля:
        name: Название подразделения
        code: Уникальный код подразделения
        parent: Родительское подразделение (для иерархии)
        head: Руководитель подразделения
        description: Описание подразделения
        created_at: Дата создания записи
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
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
        verbose_name='Родительское подразделение'
    )
    head = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Руководитель',
        related_name='headed_departments'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        db_table = 'departments_department'
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']
    
    def __str__(self):
        """Возвращает полное название подразделения с учётом иерархии."""
        if self.parent:
            return f'{self.parent} / {self.name}'
        return self.name
    
    def get_full_path(self):
        """
        Возвращает полный путь подразделения в иерархии.
        
        Returns:
            list: Список названий подразделений от корня до текущего
        """
        path = []
        current = self
        while current:
            path.insert(0, current.name)
            current = current.parent
        return path


class Employee(models.Model):
    """
    Модель сотрудника подразделения.
    
    Связывает пользователя с конкретным подразделением и должностью.
    
    Поля:
        user: Ссылка на пользователя
        department: Подразделение
        position: Должность
        employee_id: Уникальный номер сотрудника
        hire_date: Дата приёма на работу
        is_active: Активен ли сотрудник
    """
    
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name='Подразделение'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность'
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Номер сотрудника'
    )
    hire_date = models.DateField(
        verbose_name='Дата приёма'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    
    class Meta:
        db_table = 'departments_employee'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['department', 'position']
    
    def __str__(self):
        """Возвращает ФИО сотрудника и его должность."""
        return f'{self.user.get_full_name()} - {self.position}'
