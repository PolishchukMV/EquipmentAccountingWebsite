"""
Формы для приложения обратной связи.
"""

from django import forms
from .models import FeedbackMessage


class FeedbackForm(forms.ModelForm):
    """
    Форма для отправки сообщения обратной связи.
    """
    
    class Meta:
        model = FeedbackMessage
        fields = ['subject', 'message', 'email']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема обращения'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите вашу проблему или вопрос',
                'rows': 5
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
        }
    
    def clean_subject(self):
        """Проверяет длину темы сообщения."""
        subject = self.cleaned_data.get('subject')
        if len(subject) < 5:
            raise forms.ValidationError('Тема должна содержать минимум 5 символов')
        return subject
    
    def clean_message(self):
        """Проверяет длину сообщения."""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Сообщение должно содержать минимум 10 символов')
        return message