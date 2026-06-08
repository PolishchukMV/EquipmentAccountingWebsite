"""
Модели пользователей и аутентификации для системы учёта оборудования.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с ролями и связью с подразделениями.
    
    Поля:
        role: Роль пользователя в системе (администратор, менеджер, сотрудник, аудитор)
        department: Подразделение, к которому относится пользователь
        phone: Номер телефона
        avatar: Аватар пользователя
        created_at: Дата создания записи
        updated_at: Дата последнего обновления
    """
    
    # Выбор роли пользователя
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер оборудования'),
        ('employee', 'Сотрудник'),
        ('auditor', 'Аудитор'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee',
        verbose_name='Роль'
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Подразделение',
        related_name='department_users'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    # Поля для совместимости с AbstractUser
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='Группы',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='Права',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    class Meta:
        db_table = 'users_customuser'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        """Возвращает строковое представление пользователя (полное имя)."""
        return f'{self.get_full_name() or self.username}'
    
    def is_admin(self):
        """Проверяет, является ли пользователь администратором."""
        return self.role == 'admin'
    
    def is_manager(self):
        """Проверяет, является ли пользователь менеджером оборудования."""
        return self.role in ['admin', 'manager']
    
    def can_manage_equipment(self):
        """Проверяет права на управление оборудованием."""
        return self.is_manager()


class Notification(models.Model):
    """
    Модель системного уведомления для пользователя.
    
    Поля:
        user: Пользователь, которому направлено уведомление
        notification_type: Тип уведомления
        title: Заголовок уведомления
        message: Текст уведомления
        is_read: Прочитано ли уведомление
        link: Ссылка на связанную сущность
        created_at: Дата создания уведомления
    """
    
    TYPE_CHOICES = [
        ('maintenance', 'Обслуживание'),
        ('warranty', 'Гарантия'),
        ('assignment', 'Назначение'),
        ('system', 'Системное'),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Тип уведомления'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    message = models.TextField(
        verbose_name='Текст'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    link = models.URLField(
        blank=True,
        verbose_name='Ссылка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        """Возвращает заголовок уведомления."""
        return self.title
    
    def mark_as_read(self):
        """Отмечает уведомление как прочитанное."""
        self.is_read = True
        self.save()
