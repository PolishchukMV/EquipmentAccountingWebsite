"""
Представления для аутентификации и управления пользователями.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser, Notification
from .forms import CustomUserCreationForm, ProfileUpdateForm


class LoginView(DjangoLoginView):
    """
    Представление для входа пользователя в систему.
    
    Использует стандартную форму аутентификации Django с кастомными шаблонами.
    """
    
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """
        Вызывается при успешной аутентификации.
        
        Args:
            form: Форма аутентификации
            
        Returns:
            redirect: Перенаправление на целевую страницу
        """
        messages.success(self.request, f'Добро пожаловать, {self.request.user.username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Вызывается при ошибке аутентификации.
        
        Args:
            form: Форма аутентификации
            
        Returns:
            render: Перерисовка формы с ошибкой
        """
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)


class LogoutView(DjangoLogoutView):
    """
    Представление для выхода пользователя из системы.
    """
    
    template_name = 'accounts/logout.html'
    next_page = 'equipment:equipment_list'


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.
    """
    
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        """
        Вызывается при успешной валидации формы регистрации.
        
        Args:
            form: Форма регистрации
            
        Returns:
            redirect: Перенаправление на страницу входа
        """
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация успешна! Теперь вы можете войти.')
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Представление для просмотра профиля пользователя.
    """
    
    model = CustomUser
    template_name = 'accounts/profile.html'
    
    def get_object(self):
        """
        Возвращает текущего пользователя.
        
        Returns:
            CustomUser: Текущий пользователь
        """
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля пользователя.
    """
    
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """
        Возвращает текущего пользователя для редактирования.
        
        Returns:
            CustomUser: Текущий пользователь
        """
        return self.request.user
    
    def form_valid(self, form):
        """
        Вызывается при успешной валидации формы редактирования.
        
        Args:
            form: Форма редактирования профиля
            
        Returns:
            redirect: Перенаправление на страницу профиля
        """
        messages.success(self.request, 'Профиль успешно обновлён')
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, DjangoPasswordChangeView):
    """
    Представление для смены пароля пользователя.
    """
    
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        """
        Вызывается при успешной смене пароля.
        
        Args:
            form: Форма смены пароля
            
        Returns:
            redirect: Перенаправление на целевую страницу
        """
        messages.success(self.request, 'Пароль успешно изменён')
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class NotificationsView(LoginRequiredMixin, ListView):
    """
    Представление для просмотра уведомлений пользователя.
    """
    
    model = Notification
    template_name = 'accounts/notifications.html'
    context_object_name = 'notifications'
    
    def get_queryset(self):
        """
        Возвращает уведомления текущего пользователя.
        
        Returns:
            QuerySet: Уведомления текущего пользователя
        """
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


def mark_notification_read(request, pk):
    """
    Функция для отметки уведомления как прочитанного.
    
    Args:
        request: Объект запроса
        pk: ID уведомления
        
    Returns:
        redirect: Перенаправление на страницу уведомлений
    """
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    messages.success(request, 'Уведомление отмечено как прочитанное')
    return redirect('accounts:notifications')


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Панель администратора с быстрыми ссылками на CRUD операции.
    Доступна только суперпользователям.
    """
    
    template_name = 'accounts/admin_dashboard.html'
    
    def test_func(self):
        """Проверка: является ли пользователь суперпользователем"""
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        """Добавление контекстных данных"""
        context = super().get_context_data(**kwargs)
        # Здесь можно добавить статистику
        from apps.equipment.models import Equipment
        from apps.departments.models import Department
        from apps.feedback.models import FeedbackMessage
        
        context['equipment_count'] = Equipment.objects.count()
        context['department_count'] = Department.objects.count()
        context['feedback_count'] = FeedbackMessage.objects.count()
        context['user_count'] = CustomUser.objects.count()
        return context
