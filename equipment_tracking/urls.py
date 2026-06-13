"""
URL конфигурация для проекта equipment_tracking.

Главный файл маршрутизации, подключающий все приложения проекта.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Панель администратора
    path('admin/', admin.site.urls),
    
    # Приложения проекта
    path('equipment/', include('apps.equipment.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('departments/', include('apps.departments.urls')),
    path('maintenance/', include('apps.maintenance.urls')),
    path('reports/', include('apps.reports.urls')),
    path('feedback/', include('apps.feedback.urls')),
    
    # Главная страница (перенаправление на список оборудования)
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    
    # Статические страницы
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('help/', TemplateView.as_view(template_name='pages/help.html'), name='help'),
]

# Обработка медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Кастомные страницы ошибок
handler400 = 'apps.equipment.views.bad_request'
handler403 = 'apps.equipment.views.forbidden'
handler404 = 'apps.equipment.views.not_found'
handler500 = 'apps.equipment.views.server_error'
