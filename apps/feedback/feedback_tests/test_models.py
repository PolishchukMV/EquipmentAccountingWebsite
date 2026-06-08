"""
Тесты для моделей приложения feedback.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.feedback.models import FeedbackMessage


UserModel = get_user_model()


class FeedbackMessageModelTest(TestCase):
    """Тесты для модели FeedbackMessage."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.feedback_data = {
            'author': self.user,
            'email': 'test@example.com',
            'subject': 'Проблема с системой',
            'message': 'Описание проблемы',
            'status': 'new'
        }
    
    def test_create_feedback(self):
        """Тест создания сообщения обратной связи."""
        feedback = FeedbackMessage.objects.create(**self.feedback_data)
        
        self.assertEqual(feedback.author, self.user)
        self.assertEqual(feedback.email, 'test@example.com')
        self.assertEqual(feedback.subject, 'Проблема с системой')
        self.assertEqual(feedback.status, 'new')
    
    def test_feedback_string_representation(self):
        """Тест строкового представления сообщения."""
        feedback = FeedbackMessage.objects.create(**self.feedback_data)
        expected = f"testuser: Проблема с системой"
        self.assertEqual(str(feedback), expected)
    
    def test_feedback_anonymous(self):
        """Тест анонимного сообщения."""
        feedback = FeedbackMessage.objects.create(
            email='anonymous@example.com',
            subject='Анонимный вопрос',
            message='Вопрос без авторизации',
            status='new'
        )
        
        self.assertIsNone(feedback.author)
        self.assertEqual(feedback.email, 'anonymous@example.com')
    
    def test_feedback_status_choices(self):
        """Тест выбора статусов."""
        feedback = FeedbackMessage.objects.create(**self.feedback_data)
        
        statuses = [choice[0] for choice in FeedbackMessage.STATUS_CHOICES]
        self.assertIn(feedback.status, statuses)
    
    def test_feedback_mark_as_responded(self):
        """Тест отметки об ответе."""
        feedback = FeedbackMessage.objects.create(**self.feedback_data)
        
        feedback.status = 'in_progress'
        feedback.response = 'Ответ администратора'
        feedback.responded_by = self.user
        feedback.save()
        
        self.assertEqual(feedback.status, 'in_progress')
        self.assertIsNotNone(feedback.response)
        self.assertEqual(feedback.responded_by, self.user)
    
    def test_feedback_timestamps(self):
        """Тест временных меток."""
        feedback = FeedbackMessage.objects.create(**self.feedback_data)
        
        self.assertIsNotNone(feedback.timestamp)
        self.assertIsNone(feedback.responded_at)
    
    def test_feedback_unread_count(self):
        """Тест подсчёта непрочитанных сообщений."""
        FeedbackMessage.objects.create(
            email='user1@example.com',
            subject='Сообщение 1',
            message='Текст 1',
            status='new'
        )
        
        FeedbackMessage.objects.create(
            email='user2@example.com',
            subject='Сообщение 2',
            message='Текст 2',
            status='new'
        )
        
        FeedbackMessage.objects.create(
            email='user3@example.com',
            subject='Сообщение 3',
            message='Текст 3',
            status='in_progress'
        )
        
        new_count = FeedbackMessage.objects.filter(status='new').count()
        self.assertEqual(new_count, 2)