"""
Контекст-процессоры для добавления общих данных в шаблоны.
"""

def breadcrumbs(request):
    """
    Добавляет хлебные крошки в контекст шаблона.
    
    Анализирует текущий URL и строит цепочку навигации.
    
    Args:
        request: Объект запроса Django
        
    Returns:
        dict: Словарь с ключом 'breadcrumbs' - списком крошек навигации
    """
    breadcrumbs = []
    # Исключаем пустые части и специальный путь
    path_parts = [p for p in request.path.strip('/').split('/') if p and p != 'admin']
    
    current_path = ''
    labels = {
        'equipment': 'Оборудование',
        'departments': 'Подразделения',
        'maintenance': 'Обслуживание',
        'reports': 'Отчёты',
        'feedback': 'Обратная связь',
        'accounts': 'Учёт',
        'login': 'Вход',
        'logout': 'Выход',
        'profile': 'Профиль',
        'create': 'Создать',
        'update': 'Редактировать',
        'delete': 'Удалить',
        'search': 'Поиск',
        'filter': 'Фильтр',
        'history': 'История',
        'calendar': 'Календарь',
        'export': 'Экспорт',
        'import': 'Импорт',
    }
    
    # Добавляем главную
    breadcrumbs.append({
        'label': 'Главная',
        'url': '/',
        'active': len(path_parts) == 0
    })
    
    for i, part in enumerate(path_parts):
        current_path += f'/{part}'
        # Получаем метку из словаря или преобразуем часть пути
        label = labels.get(part, part.replace('-', ' ').title())
        
        breadcrumbs.append({
            'label': label,
            'url': current_path,
            'active': i == len(path_parts) - 1
        })
    
    return {'breadcrumbs': breadcrumbs}
