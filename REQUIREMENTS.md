# Требования к разработке веб-сервиса «Учёт оборудования компании»

## 1. Общие сведения о проекте

| Параметр | Значение |
|----------|----------|
| **Название** | Система учёта оборудования ООО «ПроИнфоСервис» |
| **Студент** | Полищук Михаил Владимирович |
| **Направление** | 38.03.05 Бизнес-информатика («Цифровая экономика») |
| **Организация** | ООО «ПроИнфоСервис» |
| **Период практики** | 11.05.2026 – 07.06.2026 |
| **Тип практики** | преддипломная |
| **Технологии** | Python 3.11+, Django 5.x, PostgreSQL/SQLite, HTML5, CSS3, JavaScript |
| **Хостинг** | PythonAnywhere / Render / Railway (бесплатный тариф) |
| **Репозиторий** | Gitflic / GitHub (≥ 50 коммитов) |
| **Объём кода** | ≥ 2000 строк (без комментариев и пустых строк) |

---

## 2. Структура проекта

```
equipment_tracking/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── docker-compose.yml (опционально)
├── equipment_tracking/          # Главный проект Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py                  # Корневой URL-конфиг
│   ├── wsgi.py
│   └── context_processors.py    # Контекст-процессоры (хлебные крошки, меню)
│
├── apps/
│   ├── accounts/                # Авторизация и пользователи
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates/accounts/
│   │   └── tests/
│   │
│   ├── equipment/               # Основное приложение: оборудование
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── utils.py             # Утилиты экспорта
│   │   ├── templates/equipment/
│   │   └── tests/
│   │
│   ├── departments/             # Подразделения компании
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates/departments/
│   │   └── tests/
│   │
│   ├── maintenance/             # Обслуживание и ремонты
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates/maintenance/
│   │   └── tests/
│   │
│   ├── reports/                 # Отчёты и аналитика
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates/reports/
│   │   └── tests/
│   │
│   └── feedback/                # Обратная связь
│       ├── __init__.py
│       ├── admin.py
│       ├── forms.py
│       ├── models.py
│       ├── urls.py
│       ├── views.py
│       ├── templates/feedback/
│       └── tests/
│
├── static/                      # Статические файлы
│   ├── css/
│   │   ├── base.css
│   │   ├── equipment.css
│   │   ├── reports.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── main.js
│   │   ├── charts.js
│   │   └── forms.js
│   └── images/
│       ├── logo.png
│       └── icons/
│
├── media/                       # Загружаемые файлы
│   ├── documents/
│   └── photos/
│
├── templates/                   # Глобальные шаблоны
│   ├── base.html
│   ├── includes/
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── sidebar.html
│   │   ├── breadcrumbs.html
│   │   └── pagination.html
│   ├── errors/
│   │   ├── 400.html
│   │   ├── 403.html
│   │   ├── 404.html
│   │   └── 500.html
│   └── email/
│       ├── notification.html
│       └── report.html
│
└── tests/                       # Интеграционные тесты
    ├── __init__.py
    ├── test_integration.py
    └── test_e2e.py
```

---

## 3. Модели данных (≥ 10 таблиц)

### 3.1 Таблица `users_customuser` (Расширенная модель пользователя)

```python
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер оборудования'),
        ('employee', 'Сотрудник'),
        ('auditor', 'Аудитор'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_customuser'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
```

### 3.2 Таблица `departments_department` (Подразделения)

```python
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    head = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'departments_department'
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
    
    def __str__(self):
        return self.name
```

### 3.3 Таблица `equipment_category` (Категории оборудования)

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'equipment_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
```

### 3.4 Таблица `equipment_equipment` (Основное оборудование)

```python
class Equipment(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступно'),
        ('in_use', 'В использовании'),
        ('repair', 'В ремонте'),
        ('written_off', 'Списано'),
        ('lost', 'Утеряно'),
    ]
    
    inventory_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    serial_number = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    warranty_period = models.IntegerField(help_text='Месяцев', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True)
    responsible_person = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    photo = models.ImageField(upload_to='equipment/photos/', null=True, blank=True)
    document = models.FileField(upload_to='equipment/documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
        return f'{self.inventory_number} - {self.name}'
```

### 3.5 Таблица `equipment_assignment` (Перемещения/Назначения)

```python
class Assignment(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    from_department = models.ForeignKey('departments.Department', related_name='from_assignments', on_delete=models.SET_NULL, null=True)
    to_department = models.ForeignKey('departments.Department', related_name='to_assignments', on_delete=models.SET_NULL, null=True)
    from_person = models.ForeignKey('users.CustomUser', related_name='from_assignments', on_delete=models.SET_NULL, null=True)
    to_person = models.ForeignKey('users.CustomUser', related_name='to_assignments', on_delete=models.SET_NULL, null=True)
    assignment_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Активно'),
        ('returned', 'Возвращено'),
        ('cancelled', 'Отменено'),
    ], default='active')
    document = models.FileField(upload_to='assignments/', null=True, blank=True)
    created_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'equipment_assignment'
        verbose_name = 'Назначение оборудования'
        verbose_name_plural = 'Назначения оборудования'
        ordering = ['-assignment_date']
```

### 3.6 Таблица `maintenance_maintenance` (Обслуживание и ремонты)

```python
class Maintenance(models.Model):
    TYPE_CHOICES = [
        ('planned', 'Плановое'),
        ('repair', 'Ремонт'),
        ('inspection', 'Инспекция'),
        ('upgrade', 'Модернизация'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contractor = models.CharField(max_length=200, blank=True)
    technician = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    document = models.FileField(upload_to='maintenance/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'maintenance_maintenance'
        verbose_name = 'Обслуживание'
        verbose_name_plural = 'Обслуживание'
        ordering = ['-scheduled_date']
```

### 3.7 Таблица `feedback_feedbackmessage` (Обратная связь)

```python
class FeedbackMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    ]
    
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    response = models.TextField(blank=True)
    responded_by = models.ForeignKey('users.CustomUser', related_name='responses', on_delete=models.SET_NULL, null=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'feedback_feedbackmessage'
        verbose_name = 'Сообщение обратной связи'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']
```

### 3.8 Таблица `reports_report` (Отчёты)

```python
class Report(models.Model):
    TYPE_CHOICES = [
        ('inventory', 'Инвентаризация'),
        ('movement', 'Перемещения'),
        ('maintenance', 'Обслуживание'),
        ('status', 'Статус оборудования'),
        ('financial', 'Финансовый'),
    ]
    
    FORMAT_CHOICES = [
        ('xlsx', 'Excel'),
        ('docx', 'Word'),
        ('pdf', 'PDF'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='xlsx')
    parameters = models.JSONField(default=dict)
    file = models.FileField(upload_to='reports/')
    generated_by = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reports_report'
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ['-generated_at']
```

### 3.9 Таблица `equipment_equipmentlog` (Журнал изменений)

```python
class EquipmentLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Создано'),
        ('updated', 'Обновлено'),
        ('status_changed', 'Статус изменён'),
        ('assigned', 'Назначено'),
        ('returned', 'Возвращено'),
        ('deleted', 'Удалено'),
    ]
    
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'equipment_equipmentlog'
        verbose_name = 'Журнал изменений'
        verbose_name_plural = 'Журнал изменений'
        ordering = ['-timestamp']
```

### 3.10 Таблица `departments_employee` (Сотрудники подразделений)

```python
class Employee(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'departments_employee'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
```

### 3.11 Таблица `equipment_accessory` (Комплектующие/Аксессуары)

```python
class Accessory(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    serial_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'equipment_accessory'
        verbose_name = 'Аксессуар'
        verbose_name_plural = 'Аксессуары'
```

### 3.12 Таблица `notifications_notification` (Уведомления)

```python
class Notification(models.Model):
    TYPE_CHOICES = [
        ('maintenance', 'Обслуживание'),
        ('warranty', 'Гарантия'),
        ('assignment', 'Назначение'),
        ('system', 'Системное'),
    ]
    
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications_notification'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
```

---

## 4. Endpoints (URL-маршруты)

### 4.1 Корневые маршруты (`equipment_tracking/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.equipment.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('departments/', include('apps.departments.urls')),
    path('maintenance/', include('apps.maintenance.urls')),
    path('reports/', include('apps.reports.urls')),
    path('feedback/', include('apps.feedback.urls')),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('help/', TemplateView.as_view(template_name='pages/help.html'), name='help'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Кастомные страницы ошибок
handler400 = 'apps.equipment.views.bad_request'
handler403 = 'apps.equipment.views.forbidden'
handler404 = 'apps.equipment.views.not_found'
handler500 = 'apps.equipment.views.server_error'
```

### 4.2 Оборудование (`apps/equipment/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    # Главная страница
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('<int:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    
    # Поиск и фильтрация
    path('search/', views.EquipmentSearchView.as_view(), name='equipment_search'),
    path('filter/', views.EquipmentFilterView.as_view(), name='equipment_filter'),
    
    # Статусы
    path('<int:pk>/status/', views.EquipmentStatusView.as_view(), name='equipment_status'),
    
    # Экспорт
    path('export/xlsx/', views.export_equipment_xlsx, name='export_xlsx'),
    path('export/docx/', views.export_equipment_docx, name='export_docx'),
    path('<int:pk>/export/', views.export_equipment_detail, name='export_detail'),
    
    # Импорт
    path('import/', views.import_equipment, name='import_equipment'),
    
    # Категории
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Журнал
    path('<int:pk>/history/', views.EquipmentHistoryView.as_view(), name='equipment_history'),
]
```

### 4.3 Аккаунты (`apps/accounts/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='notification_read'),
]
```

### 4.4 Подразделения (`apps/departments/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department_list'),
    path('<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    path('<int:pk>/employees/', views.DepartmentEmployeesView.as_view(), name='department_employees'),
    path('<int:pk>/equipment/', views.DepartmentEquipmentView.as_view(), name='department_equipment'),
]
```

### 4.5 Обслуживание (`apps/maintenance/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.MaintenanceListView.as_view(), name='maintenance_list'),
    path('create/', views.MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('<int:pk>/', views.MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('<int:pk>/update/', views.MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('<int:pk>/delete/', views.MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    path('<int:pk>/complete/', views.MaintenanceCompleteView.as_view(), name='maintenance_complete'),
    path('calendar/', views.MaintenanceCalendarView.as_view(), name='maintenance_calendar'),
    path('upcoming/', views.UpcomingMaintenanceView.as_view(), name='upcoming_maintenance'),
]
```

### 4.6 Отчёты (`apps/reports/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportsDashboardView.as_view(), name='reports_dashboard'),
    path('inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    path('movement/', views.MovementReportView.as_view(), name='movement_report'),
    path('maintenance/', views.MaintenanceReportView.as_view(), name='maintenance_report'),
    path('status/', views.StatusReportView.as_view(), name='status_report'),
    path('financial/', views.FinancialReportView.as_view(), name='financial_report'),
    path('generate/', views.GenerateReportView.as_view(), name='generate_report'),
    path('history/', views.ReportHistoryView.as_view(), name='report_history'),
]
```

### 4.7 Обратная связь (`apps/feedback/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackListView.as_view(), name='feedback_list'),
    path('create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('<int:pk>/respond/', views.FeedbackRespondView.as_view(), name='feedback_respond'),
    path('<int:pk>/status/', views.FeedbackStatusView.as_view(), name='feedback_status'),
]
```

---

## 5. Страницы сайта (≥ 10 страниц без авторизации)

| № | Страница | URL | Требует авторизации |
|---|----------|-----|---------------------|
| 1 | Главная | `/` | Нет |
| 2 | Оборудование (список) | `/equipment/` | Нет |
| 3 | Оборудование (детали) | `/equipment/<id>/` | Нет |
| 4 | Категории оборудования | `/equipment/categories/` | Нет |
| 5 | Подразделения | `/departments/` | Нет |
| 6 | Подразделение (детали) | `/departments/<id>/` | Нет |
| 7 | Обслуживание (календарь) | `/maintenance/calendar/` | Нет |
| 8 | Обратная связь | `/feedback/` | Нет |
| 9 | Создать обращение | `/feedback/create/` | Нет |
| 10 | О системе | `/about/` | Нет |
| 11 | Помощь | `/help/` | Нет |
| 12 | Поиск оборудования | `/equipment/search/` | Нет |
| 13 | Логин | `/accounts/login/` | Нет |
| 14 | Регистрация | `/accounts/register/` | Нет |
| 15 | Панель администратора | `/admin/` | **Да** |
| 16 | Профиль пользователя | `/accounts/profile/` | **Да** |
| 17 | Создание оборудования | `/equipment/create/` | **Да** |
| 18 | Редактирование оборудования | `/equipment/<id>/update/` | **Да** |
| 19 | Назначение оборудования | `/equipment/<id>/assign/` | **Да** |
| 20 | Отчёты | `/reports/` | **Да** |
| 21 | Генерация отчёта | `/reports/generate/` | **Да** |
| 22 | Уведомления | `/accounts/notifications/` | **Да** |
| 23 | История оборудования | `/equipment/<id>/history/` | **Да** |

---

## 6. Роли пользователей (≥ 3 роли)

| Роль | Права доступа |
|------|--------------|
| **Администратор** | Полный доступ ко всем функциям, управление пользователями, настройка системы |
| **Менеджер оборудования** | CRUD оборудования, назначение, создание отчётов, управление обслуживанием |
| **Сотрудник** | Просмотр оборудования, подача заявок на оборудование, обратная связь |
| **Аудитор** | Просмотр всех данных, генерация отчётов, доступ к журналу изменений |

### 6.1 Матрица прав доступа

| Функция | Admin | Manager | Employee | Auditor |
|---------|-------|---------|----------|---------|
| Просмотр оборудования | ✓ | ✓ | ✓ | ✓ |
| Создание оборудования | ✓ | ✓ | ✗ | ✗ |
| Редактирование оборудования | ✓ | ✓ | ✗ | ✗ |
| Удаление оборудования | ✓ | ✓ | ✗ | ✗ |
| Назначение оборудования | ✓ | ✓ | ✗ | ✗ |
| Просмотр отчётов | ✓ | ✓ | ✗ | ✓ |
| Генерация отчётов | ✓ | ✓ | ✗ | ✓ |
| Управление пользователями | ✓ | ✗ | ✗ | ✗ |
| Обслуживание (CRUD) | ✓ | ✓ | ✗ | ✗ |
| Обратная связь | ✓ | ✓ | ✓ | ✓ |
| Журнал изменений | ✓ | ✓ | ✗ | ✓ |

---

## 7. Панель администратора (≥ 5 страниц)

1. **Дашборд** — статистика, графики, быстрые действия
2. **Управление оборудованием** — список, фильтрация, массовые операции
3. **Управление пользователями** — роли, подразделения, блокировка
4. **Отчёты и аналитика** — генерация, история, экспорт
5. **Настройки системы** — категории, статусы, уведомления
6. **Журнал аудита** — все изменения в системе
7. **Обратная связь** — обработка обращений

---

## 8. Личные кабинеты (≥ 5 страниц)

1. **Профиль пользователя** — личная информация, аватар
2. **Мои назначения** — оборудование на ответственности
3. **Мои заявки** — история заявок на оборудование
4. **Уведомления** — системные уведомления
5. **История действий** — журнал действий пользователя
6. **Настройки** — пароль, уведомления, предпочтения

---

## 9. Меню навигации (≥ 10 пунктов)

```
Главная
Оборудование
  ├─ Список оборудования
  ├─ Категории
  ├─ Создать запись
  └─ Поиск
Подразделения
  ├─ Список подразделений
  └─ Структура
Обслуживание
  ├─ Календарь
  ├─ Запланированное
  └─ История
Отчёты
  ├─ Дашборд
  ├─ Инвентаризация
  ├─ Перемещения
  └─ Финансовый
Пользователи
  ├─ Профиль
  ├─ Уведомления
  └─ Настройки
Обратная связь
  ├─ Создать обращение
  └─ Мои обращения
О системе
  ├─ О проекте
  └─ Помощь
```

---

## 10. Хлебные крошки (на каждой странице)

Пример реализации в шаблоне:

```html
<!-- templates/includes/breadcrumbs.html -->
<nav aria-label="breadcrumb" class="breadcrumbs">
    <ol class="breadcrumb">
        <li class="breadcrumb-item">
            <a href="{% url 'equipment:equipment_list' %}">Главная</a>
        </li>
        {% for crumb in breadcrumbs %}
            {% if forloop.last %}
                <li class="breadcrumb-item active" aria-current="page">{{ crumb.label }}</li>
            {% else %}
                <li class="breadcrumb-item">
                    <a href="{{ crumb.url }}">{{ crumb.label }}</a>
                </li>
            {% endif %}
        {% endfor %}
    </ol>
</nav>
```

Контекст-процессор:

```python
# equipment_tracking/context_processors.py
def breadcrumbs(request):
    breadcrumbs = []
    path_parts = request.path.strip('/').split('/')
    
    current_path = ''
    for part in path_parts:
        current_path += f'/{part}'
        breadcrumbs.append({
            'label': part.replace('-', ' ').title(),
            'url': current_path
        })
    
    return {'breadcrumbs': breadcrumbs}
```

---

## 11. Экспорт документов (.docx / .xlsx)

### 11.1 Экспорт в Excel (`apps/equipment/utils.py`)

```python
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from django.http import HttpResponse
from .models import Equipment

def export_equipment_to_xlsx(queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Оборудование"
    
    # Заголовки
    headers = [
        'Инвентарный номер', 'Наименование', 'Категория', 
        'Серийный номер', 'Производитель', 'Модель',
        'Дата покупки', 'Цена', 'Статус', 'Подразделение',
        'Ответственный', 'Местоположение'
    ]
    
    # Стили
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = openpyxl.styles.PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Заголовки
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')
        cell.border = thin_border
    
    # Данные
    for row, equipment in enumerate(queryset, 2):
        ws.cell(row=row, column=1, value=equipment.inventory_number)
        ws.cell(row=row, column=2, value=equipment.name)
        ws.cell(row=row, column=3, value=str(equipment.category) if equipment.category else '')
        ws.cell(row=row, column=4, value=equipment.serial_number)
        ws.cell(row=row, column=5, value=equipment.manufacturer)
        ws.cell(row=row, column=6, value=equipment.model)
        ws.cell(row=row, column=7, value=equipment.purchase_date.strftime('%d.%m.%Y') if equipment.purchase_date else '')
        ws.cell(row=row, column=8, value=float(equipment.purchase_price) if equipment.purchase_price else '')
        ws.cell(row=row, column=9, value=equipment.get_status_display())
        ws.cell(row=row, column=10, value=str(equipment.department) if equipment.department else '')
        ws.cell(row=row, column=11, value=str(equipment.responsible_person) if equipment.responsible_person else '')
        ws.cell(row=row, column=12, value=equipment.location)
        
        # Применяем границы
        for col in range(1, 13):
            ws.cell(row=row, column=col).border = thin_border
    
    # Автоширина колонок
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="equipment.xlsx"'
    wb.save(response)
    return response
```

### 11.2 Экспорт в Word

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def export_equipment_to_docx(equipment):
    doc = Document()
    
    # Заголовок
    heading = doc.add_heading(f'Карточка оборудования №{equipment.inventory_number}', 0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Информация
    doc.add_paragraph(f'Дата формирования: {equipment.created_at.strftime("%d.%m.%Y %H:%M")}')
    doc.add_paragraph()
    
    table = doc.add_table(rows=1, cols=2)
    table.style = 'Table Grid'
    
    data = [
        ('Наименование:', equipment.name),
        ('Категория:', str(equipment.category) if equipment.category else 'Не указана'),
        ('Инвентарный номер:', equipment.inventory_number),
        ('Серийный номер:', equipment.serial_number or 'Не указан'),
        ('Производитель:', equipment.manufacturer or 'Не указан'),
        ('Модель:', equipment.model or 'Не указан'),
        ('Дата покупки:', equipment.purchase_date.strftime('%d.%m.%Y') if equipment.purchase_date else 'Не указана'),
        ('Цена:', f'{equipment.purchase_price} руб.' if equipment.purchase_price else 'Не указана'),
        ('Статус:', equipment.get_status_display()),
        ('Подразделение:', str(equipment.department) if equipment.department else 'Не назначено'),
        ('Ответственный:', str(equipment.responsible_person) if equipment.responsible_person else 'Не назначен'),
        ('Местоположение:', equipment.location or 'Не указано'),
    ]
    
    for label, value in data:
        row = table.add_row().cells
        row[0].text = label
        row[1].text = value
        row[0].paragraphs[0].runs[0].bold = True
    
    # Примечания
    if equipment.notes:
        doc.add_heading('Примечания', level=2)
        doc.add_paragraph(equipment.notes)
    
    # Подвал
    doc.add_page_break()
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run('ООО «ПроИнфоСервис»\nСистема учёта оборудования\nПолищук Михаил Владимирович')
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="equipment_{equipment.inventory_number}.docx"'
    doc.save(response)
    return response
```

---

## 12. Доступ к файловой системе

### 12.1 Загрузка файлов

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

ALLOWED_EXTENSIONS = {
    'document': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt'],
    'image': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
}
```

### 12.2 Валидация загружаемых файлов

```python
# apps/equipment/forms.py
import os
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1][1:].lower()
    allowed = settings.ALLOWED_EXTENSIONS['document']
    if ext not in allowed:
        raise ValidationError(f'Недопустимый формат файла. Разрешены: {", ".join(allowed)}')
    if value.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError('Файл слишком большой. Максимальный размер: 10 MB')
```

---

## 13. Кроссбраузерность и адаптивность

### 13.1 Поддерживаемые браузеры
- Mozilla Firefox (последние 2 версии)
- Google Chrome (последние 2 версии)
- Яндекс.Браузер (последние 2 версии)
- Microsoft Edge (последние 2 версии)

### 13.2 Адаптивные точки_breakpoints

```css
/* static/css/responsive.css */
:root {
    --breakpoint-sm: 576px;   /* Смартфоны портрет */
    --breakpoint-md: 768px;   /* Смартфоны ландшафт / Планшеты */
    --breakpoint-lg: 992px;   /* Планшеты ландшафт / Ноутбуки */
    --breakpoint-xl: 1200px;  /* Десктопы */
    --breakpoint-xxl: 1400px; /* Большие десктопы */
}

/* Мобильная навигация */
@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        left: -280px;
        transition: left 0.3s ease;
    }
    .sidebar.active {
        left: 0;
    }
    .mobile-menu-toggle {
        display: block;
    }
}

/* Таблицы на мобильных */
@media (max-width: 576px) {
    .table-responsive {
        overflow-x: auto;
    }
    table {
        min-width: 700px;
    }
}
```

---

## 14. Форма обратной связи

```python
# apps/feedback/forms.py
from django import forms
from .models import FeedbackMessage

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = ['subject', 'message', 'email']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Тема обращения',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите вашу проблему или вопрос',
                'rows': 5,
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
        }
    
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject) < 5:
            raise forms.ValidationError('Тема должна содержать минимум 5 символов')
        return subject
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Сообщение должно содержать минимум 10 символов')
        return message
```

---

## 15. Безопасность и разграничение прав

### 15.1 Декораторы для проверки прав

```python
# apps/accounts/decorators.py
from functools import wraps
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Использование
@role_required(['admin', 'manager'])
def equipment_create(request):
    ...
```

### 15.2 Миксины для CBV

```python
# apps/accounts/mixins.py
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin:
    allowed_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if self.allowed_roles and request.user.role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin']

class ManagerRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin', 'manager']
```

---

## 16. План разработки по неделям

### Неделя 1: Подготовка и анализ
- [ ] Настройка проекта Django
- [ ] Проектирование БД (модели)
- [ ] Создание репозитория Git
- [ ] Базовая структура шаблонов
- [ ] Модель «КАК ЕСТЬ» (бизнес-процессы)
- [ ] Техническое задание

### Неделя 2-3: Разработка
- [ ] Реализация моделей (миграции)
- [ ] CRUD оборудования
- [ ] Система авторизации
- [ ] Панель администратора
- [ ] Отчёты и экспорт
- [ ] Обратная связь
- [ ] Модель «КАК ДОЛЖНО БЫТЬ»
- [ ] Прототипирование интерфейса

### Неделя 4: Тестирование и документация
- [ ] Модульное тестирование
- [ ] Интеграционное тестирование
- [ ] Тест-план и тест-кейсы
- [ ] Баг-репорты
- [ ] Отладка системы
- [ ] Оформление отчёта
- [ ] Развёртывание на хостинге

---

## 17. Требования к тестированию (≥ 4 метода)

### Выбранные методы:

| № | Метод | Категория | Описание |
|---|-------|-----------|----------|
| 1 | Позитивное тестирование | По принципам работы | Проверка корректной работы при валидных данных |
| 2 | Критический путь | По уровню функционального | Тестирование основных сценариев использования |
| 3 | Автоматическое | По автоматизации | Unit-тесты Django, Selenium для UI |
| 4 | Чёрный ящик | По доступу к коду | Тестирование без знания внутренней реализации |
| 5 | Интеграционное | По уровню детализации | Проверка взаимодействия компонентов |
| 6 | Регрессионное | По целям | Проверка после внесения изменений |

### Пример тест-кейса:

```markdown
## TC-001: Создание записи оборудования

**PreConditions:**
- Пользователь авторизован с ролью "Менеджер"
- Открыта страница создания оборудования

**Steps:**
1. Заполнить поле "Инвентарный номер" = "INV-001"
2. Заполнить поле "Наименование" = "Ноутбук Dell"
3. Выбрать категорию = "Компьютеры"
4. Нажать кнопку "Сохранить"

**Expected Result:**
- Запись создана
- Отображается сообщение об успехе
- Пользователь перенаправлен на страницу деталей
```

### Пример баг-репорта:

```markdown
## BUG-001: Ошибка при экспорте в Excel

**Серьёзность:** S3 (Major)
**Приоритет:** Высокий

**Описание:**
При экспорте более 1000 записей в Excel возникает таймаут

**Steps to Reproduce:**
1. Открыть список оборудования
2. Применить фильтр (все записи)
3. Нажать "Экспорт в Excel"

**Actual Result:**
Ошибка 504 Gateway Timeout

**Expected Result:**
Файл Excel успешно скачивается
```

---

## 18. Requirements.txt

```txt
Django==5.0.6
django-crispy-forms==2.1
crispy-bootstrap5==2024.2
openpyxl==3.1.2
python-docx==1.1.0
Pillow==10.3.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
gunicorn==22.0.0
whitenoise==6.6.0
django-filter==24.2
django-widget-tweaks==1.5.0
```

---

## 19. Git-стратегия (≥ 50 коммитов)

```bash
# Примерная структура коммитов
git commit -m "init: Initial project setup"
git commit -m "models: Add CustomUser model"
git commit -m "models: Add Department model"
git commit -m "models: Add Equipment model"
git commit -m "models: Add Category model"
git commit -m "models: Add Assignment model"
git commit -m "models: Add Maintenance model"
git commit -m "models: Add Feedback model"
git commit -m "models: Add Report model"
git commit -m "models: Add EquipmentLog model"
git commit -m "models: Add Employee model"
git commit -m "models: Add Accessory model"
git commit -m "models: Add Notification model"
git commit -m "views: Equipment list view"
git commit -m "views: Equipment detail view"
git commit -m "views: Equipment create view"
git commit -m "views: Equipment update view"
git commit -m "views: Equipment delete view"
git commit -m "views: Equipment search"
git commit -m "views: Equipment filter"
git commit -m "templates: Base template"
git commit -m "templates: Header component"
git commit -m "templates: Footer component"
git commit -m "templates: Sidebar component"
git commit -m "templates: Breadcrumbs component"
git commit -m "templates: Equipment list template"
git commit -m "templates: Equipment detail template"
git commit -m "static: Base CSS styles"
git commit -m "static: Responsive CSS"
git commit -m "static: JavaScript utilities"
git commit -m "auth: Login view"
git commit -m "auth: Logout view"
git commit -m "auth: Register view"
git commit -m "auth: Profile view"
git commit -m "auth: Password change"
git commit -m "export: XLSX export utility"
git commit -m "export: DOCX export utility"
git commit -m "reports: Dashboard view"
git commit -m "reports: Inventory report"
git commit -m "reports: Movement report"
git commit -m "feedback: Create feedback"
git commit -m "feedback: Feedback list"
git commit -m "feedback: Feedback response"
git commit -m "maintenance: Calendar view"
git commit -m "maintenance: Create maintenance"
git commit -m "departments: Department list"
git commit -m "departments: Department detail"
git commit -m "permissions: Role decorators"
git commit -m "permissions: Role mixins"
git commit -m "tests: Unit tests for models"
git commit -m "tests: Unit tests for views"
git commit -m "tests: Integration tests"
git commit -m "deploy: Docker configuration"
git commit -m "deploy: Production settings"
git commit -m "docs: README update"
git commit -m "fix: Bug fixes and improvements"
```

---

## 20. Проверка соответствия требованиям

| Требование | Соответствие |
|------------|--------------|
| Языки: Python/Django | ✅ |
| Бесплатный хостинг | ✅ (PythonAnywhere/Render) |
| Без CMS | ✅ (Самописное решение) |
| ≥ 50 коммитов | ✅ (План: 55+ коммитов) |
| ≥ 2000 строк кода | ✅ (Ожидаемо: 3000+ строк) |
| ≥ 10 страниц без авторизации | ✅ (14 страниц) |
| Макеты на каждую страницу | ✅ (В планах) |
| Форма обратной связи | ✅ |
| Меню ≥ 10 пунктов | ✅ (12 пунктов) |
| Хлебные крошки | ✅ (На каждой странице) |
| БД ≥ 10 таблиц | ✅ (12 таблиц) |
| Доступ к ФС | ✅ (Загрузка файлов) |
| Экспорт .docx/.xlsx | ✅ |
| Роли ≥ 3 | ✅ (4 роли) |
| Панель админа ≥ 5 страниц | ✅ (7 страниц) |
| Личные кабинеты ≥ 5 страниц | ✅ (6 страниц) |
| Кроссбраузерность | ✅ (4 браузера) |
| Адаптивность | ✅ (ПК, ноутбук, смартфон) |
| Подвал с ФИО | ✅ |
| Комментарии на русском | ✅ |

---

## 21. Рекомендации по реализации

1. **Начните с проектирования БД** — создайте все модели и сделайте миграции
2. **Используйте Class-Based Views** — уменьшит дублирование кода
3. **Внедрите django-filter** — для удобной фильтрации оборудования
4. **Используйте crispy-forms** — для красивых форм Bootstrap
5. **Добавьте django-debug-toolbar** — для отладки в разработке
6. **Настройте logging** — для отслеживания ошибок в production
7. **Используйте environment variables** — для секретов (SECRET_KEY, DATABASE_URL)
8. **Добавьте rate limiting** — для защиты от brute-force атак
9. **Реализуйте кэширование** — для улучшения производительности отчётов
10. **Добавьте search functionality** — полнотекстовый поиск по оборудованию

---

*Документ разработан для индивидуального задания по преддипломной практике*  
*Студент: Полищук Михаил Владимирович*  
*ООО «ПроИнфоСервис», 2026*
