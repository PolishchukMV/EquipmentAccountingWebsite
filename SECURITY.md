# Безопасность проекта Equipment Accounting System

## 🔒 Проверка безопасности

Для запуска проверки безопасности выполните:

```bash
python security_checks.py
```

## 📋 Список проверок

### Критические проблемы (должны быть исправлены):

- [x] ALLOWED_HOSTS не должен быть `['*']`
- [x] SECRET_KEY не должен использовать insecure-значение
- [x] .env должен быть в .gitignore
- [x] db.sqlite3 должен быть в .gitignore

### Предупреждения (рекомендуется исправить):

- [ ] DEBUG = False в production
- [ ] CSRF_COOKIE_SECURE = True в production
- [ ] SESSION_COOKIE_SECURE = True в production
- [ ] SECURE_SSL_REDIRECT = True в production

## 🛡️ Настройки безопасности

### 1. Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DJANGO_SECRET_KEY=your-super-secret-key-change-this
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
```

### 2. Секретный ключ

**НИКОГДА** не используйте default SECRET_KEY в production!

Генерация безопасного ключа:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 3. Пароли пользователей

Система использует стандартные валидаторы Django:
- UserAttributeSimilarityValidator
- MinimumLengthValidator
- CommonPasswordValidator
- NumericPasswordValidator

### 4. CSRF защита

- CSRF middleware включён по умолчанию
- Все формы содержат `{% csrf_token %}`
- CSRF токены проверяются на сервере

### 5. XSS защита

- escape() используется для пользовательского ввода в формах
- Django автоматически экранирует шаблоны
- SECURE_BROWSER_XSS_FILTER = True

### 6. Clickjacking защита

- X_FRAME_OPTIONS = 'DENY'
- Предотвращает встраивание сайта в iframe

### 7. Content Type Sniffing защита

- SECURE_CONTENT_TYPE_NOSNIFF = True
- Браузер не будет пытаться определить тип контента

## 📁 Безопасность файлов

### Загружаемые файлы

Максимальный размер: 10 MB

Разрешённые расширения:
- **Изображения**: jpg, jpeg, png, gif, webp
- **Документы**: pdf, doc, docx, xls, xlsx, txt

Валидация:
- Проверка размера файла
- Проверка расширения
- Проверка MIME-типа (рекомендуется добавить)

### Хранение файлов

- Фото: `media/equipment/photos/`
- Документы: `media/equipment/documents/`
- Назначения: `media/assignments/`

## 🔐 Аутентификация и авторизация

### Роли пользователей

1. **Admin** - полный доступ ко всему
2. **Manager** - управление оборудованием
3. **Employee** - просмотр своего оборудования
4. **Auditor** - просмотр отчётов и аудит

### Проверки прав

Все CRUD операции защищены:
- `PermissionRequiredMixin`
- `LoginRequiredMixin`
- Проверка на уровне views

## 📊 Аудит и логирование

### Журнал изменений

Все изменения оборудования логируются в `EquipmentLog`:
- Кто изменил (user)
- Что изменил (action)
- Старое значение (old_value)
- Новое значение (new_value)
- Время изменения (timestamp)

### Рекомендации

- Регулярно проверяйте логи
- Настраивайте алерты на критичные действия
- Храните логи минимум 90 дней

## 🚨 Уязвимости

### Известные уязвимости (исправлены):

1. **XSS в формах** - добавлен escape()
2. **Отсутствие валидации** - добавлены формы с валидацией
3. **fields = '__all__'** - заменено на form_class
4. **DEBUG = True** - теперь из .env

### Потенциальные уязвимости:

1. **SQL Injection** - Django ORM защищает автоматически
2. **Mass Assignment** - формы контролируют поля
3. **Directory Traversal** - FileField защищает Django

## 🔄 Обновления

### Регулярные задачи

- [ ] Обновлять Django до последней версии
- [ ] Обновлять зависимости (pip list --outdated)
- [ ] Проверять CVE для используемых пакетов
- [ ] Обновлять зависимости безопасности

### Рекомендуемые пакеты

```bash
pip install django-axes  # Защита от brute-force
pip install django-csp   # Content Security Policy
pip install bleach       # Очистка HTML
```

## 📞 Отчёт об уязвимостях

Если вы обнаружили уязвимость, пожалуйста:
1. Не публикуйте её публично
2. Сообщите разработчику
3. Дайте время на исправление

## ✅ Чеклист перед продакшеном

- [ ] DEBUG = False
- [ ] SECRET_KEY из .env
- [ ] ALLOWED_HOSTS настроен
- [ ] HTTPS включён
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] Database использует PostgreSQL
- [ ] Static files собраны (collectstatic)
- [ ] .env в .gitignore
- [ ] База данных бэкапится
- [ ] Логирование настроено
- [ ] Мониторинг включён

## 📚 Ресурсы

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)