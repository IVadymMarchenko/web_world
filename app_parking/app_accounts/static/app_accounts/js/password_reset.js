document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('id_email');
    const resetButton = document.querySelector('.btn');

    // Проверяем, что элементы найдены
    if (!emailInput || !resetButton) {
        console.error('Элементы не найдены');
        return;
    }

    // Функция для проверки заполненности поля
    function toggleButtonState() {
        // Проверка на наличие значения в поле
        if (emailInput.value.trim() !== '') {
            resetButton.removeAttribute('disabled');
            resetButton.classList.remove('disabled-button'); // Удаляем класс для неактивной кнопки
            resetButton.classList.add('btn-success'); // Добавляем класс для активной кнопки
        } else {
            resetButton.setAttribute('disabled', 'true');
            resetButton.classList.add('disabled-button'); // Добавляем класс для неактивной кнопки
            resetButton.classList.remove('btn-success'); // Удаляем класс для активной кнопки
        }
    }

    // Слушатель события для ввода данных
    emailInput.addEventListener('input', toggleButtonState);

    // Инициализация состояния кнопки при загрузке страницы
    toggleButtonState();
});


window.addEventListener('load', function() {
    // Проверяем, была ли страница обновлена
    if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(function(form) {
            // Получаем все видимые поля формы, кроме скрытых полей (например, CSRF-токенов)
            const inputs = form.querySelectorAll('input:not([type="hidden"]), textarea, select');
            
            // Очищаем значения всех видимых полей
            inputs.forEach(function(input) {
                input.value = '';
            });

            // Убираем текст ошибок, если он отображается в элементах с классом .error
            const errors = form.querySelectorAll('.error');
            errors.forEach(function(error) {
                error.innerText = '';
            });
        });
    }
});



window.addEventListener('load', function() {
    // Проверяем, была ли страница обновлена
    if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
        // Очистка сообщений
        const messageContainer = document.getElementById('messages');
        if (messageContainer) {
            messageContainer.innerHTML = '';
        }

        // Очистка ошибок формы
        const errorContainer = document.getElementById('form-errors');
        if (errorContainer) {
            errorContainer.innerHTML = '';
        }
    }
});
