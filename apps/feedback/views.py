"""
Представления для приложения обратной связи.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import FeedbackMessage
from .forms import FeedbackForm


class FeedbackListView(ListView):
    """Список сообщений обратной связи."""
    model = FeedbackMessage
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedback_messages'


class FeedbackDetailView(DetailView):
    """Детали сообщения обратной связи."""
    model = FeedbackMessage
    template_name = 'feedback/feedback_detail.html'
    context_object_name = 'feedback'


class FeedbackCreateView(CreateView):
    """Создание сообщения обратной связи."""
    model = FeedbackMessage
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback:feedback_list')
    
    def form_valid(self, form):
        """Сохраняет автора сообщения."""
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        return super().form_valid(form)


class FeedbackRespondView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Ответ на сообщение обратной связи."""
    model = FeedbackMessage
    template_name = 'feedback/feedback_respond.html'
    permission_required = 'feedback.change_feedbackmessage'
    
    def post(self, request, pk):
        feedback = self.get_object()
        feedback.response = request.POST.get('response')
        feedback.responded_by = request.user
        feedback.status = 'in_progress'
        feedback.save()
        messages.success(request, 'Ответ отправлен')
        return redirect('feedback:feedback_detail', pk=pk)


class FeedbackStatusView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Изменение статуса сообщения обратной связи."""
    model = FeedbackMessage
    fields = ['status']
    template_name = 'feedback/feedback_status.html'
    permission_required = 'feedback.change_feedbackmessage'
