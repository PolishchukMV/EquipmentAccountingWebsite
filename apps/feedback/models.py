"""
Модели обратной связи для системы.
"""

from django.db import models


class FeedbackMessage(models.Model):
    """
    Сообщение обратной связи от пользователя.
    
    Позволяет пользователям отправлять сообщения и вопросы в поддержку.
    
    Поля:
        author: Автор сообщения (пользователь)
        email: Email автора (для анонимных сообщений)
        subject: Тема сообщения
        message: Текст сообщения
        status: Статус обработки
        response: Ответ поддержки
        responded_by: Сотрудник, ответивший на сообщение
        responded_at: Дата ответа
        created_at: Дата создания сообщения
    """
    
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    ]
    
    author = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Автор'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email'
    )
    subject = models.CharField(
        max_length=200,
        verbose_name='Тема'
    )
    message = models.TextField(
        verbose_name='Сообщение'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    response = models.TextField(
        blank=True,
        verbose_name='Ответ'
    )
    responded_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responses',
        verbose_name='Ответил'
    )
    responded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата ответа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        db_table = 'feedback_feedbackmessage'
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']
    
    def __str__(self):
        """Возвращает тему сообщения."""
        return self.subject
    
    def is_resolved(self):
        """Проверяет, решена ли проблема."""
        return self.status in ['resolved', 'closed']
