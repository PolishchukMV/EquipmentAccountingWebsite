/**
 * Основной JavaScript для системы учёта оборудования
 * Author: Полищук Михаил Владимирович
 */

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Система учёта оборудования загружена');
    
    // Автоматическое скрытие алертов через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirmDelete || 'Вы уверены, что хотите удалить эту запись?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
});

// Функция для форматирования даты
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('ru-RU', options);
}

// Функция для форматирования валюты
function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
    }).format(amount);
}
