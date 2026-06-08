"""
Тесты для views приложения feedback.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.feedback.models import FeedbackMessage


UserModel = get_user_model()


class FeedbackListViewTest(TestCase):
    """Тесты для списка сообщений обратной связи."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        
        FeedbackMessage.objects.create(
            email='user1@example.com',
            subject='Сообщение 1',
            message='Текст сообщения 1',
            status='new'
        )
        
        FeedbackMessage.objects.create(
            email='user2@example.com',
            subject='Сообщение 2',
            message='Текст сообщения 2',
            status='in_progress'
        )
        
        self.url = reverse('feedback:feedback_list')
    
    def test_list_page_loads(self):
        """Тест загрузки страницы списка."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/feedback_list.html')
    
    def test_list_shows_messages(self):
        """Тест отображения сообщений."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Сообщение 1')
        self.assertContains(response, 'Сообщение 2')
    
    def test_list_context(self):
        """Тест контекста страницы списка."""
        response = self.client.get(self.url)
        
        self.assertIn('feedback_messages', response.context)
        self.assertEqual(len(response.context['feedback_messages']), 2)


class FeedbackCreateViewTest(TestCase):
    """Тесты для создания сообщения обратной связи."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        self.url = reverse('feedback:feedback_create')
        
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_page_loads(self):
        """Тест загрузки страницы создания."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/feedback_form.html')
    
    def test_create_feedback_authenticated(self):
        """Тест создания сообщения авторизованным пользователем."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(self.url, {
            'subject': 'Новое сообщение',
            'email': 'test@example.com',
            'message': 'Текст нового сообщения'
        })
        
        self.assertRedirects(response, reverse('feedback:feedback_list'))
        self.assertEqual(FeedbackMessage.objects.count(), 1)
        
        feedback = FeedbackMessage.objects.first()
        self.assertEqual(feedback.author, self.user)
        self.assertEqual(feedback.status, 'new')
    
    def test_create_feedback_anonymous(self):
        """Тест создания анонимного сообщения."""
        response = self.client.post(self.url, {
            'subject': 'Анонимное сообщение',
            'email': 'anon@example.com',
            'message': 'Текст анонимного сообщения'
        })
        
        self.assertRedirects(response, reverse('feedback:feedback_list'))
        self.assertEqual(FeedbackMessage.objects.count(), 1)
        
        feedback = FeedbackMessage.objects.first()
        self.assertIsNone(feedback.author)
    
    def test_create_feedback_empty_subject(self):
        """Тест создания с пустой темой."""
        response = self.client.post(self.url, {
            'subject': '',
            'email': 'test@example.com',
            'message': 'Текст сообщения'
        })
        
        # Форма должна быть невалидной
        self.assertEqual(response.status_code, 200)
    
    def test_create_feedback_short_message(self):
        """Тест создания с коротким сообщением."""
        response = self.client.post(self.url, {
            'subject': 'Тест',
            'email': 'test@example.com',
            'message': 'Коротко'
        })
        
        # Форма должна быть невалидной
        self.assertEqual(response.status_code, 200)


class FeedbackDetailViewTest(TestCase):
    """Тесты для деталей сообщения обратной связи."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.client = Client()
        
        self.feedback = FeedbackMessage.objects.create(
            email='user@example.com',
            subject='Тема сообщения',
            message='Текст сообщения',
            status='new'
        )
        
        self.url = reverse('feedback:feedback_detail', kwargs={'pk': self.feedback.pk})
    
    def test_detail_page_loads(self):
        """Тест загрузки страницы деталей."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/feedback_detail.html')
    
    def test_detail_shows_info(self):
        """Тест отображения информации."""
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Тема сообщения')
        self.assertContains(response, 'Текст сообщения')