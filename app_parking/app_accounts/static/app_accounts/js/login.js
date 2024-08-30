document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById('id_email'); // Поле для ввода email или логина
    const passwordInput = document.getElementById('id_password'); // Поле для ввода пароля
    const loginButton = document.querySelector('.button'); // Кнопка входа

    // Проверяем, что элементы найдены
    if (!emailInput || !passwordInput || !loginButton) {
        console.error('Элементы формы не найдены');
        return;
    }

    // Функция для включения/отключения кнопки
    function toggleButtonState() {
        // Проверяем, что оба поля не пустые
        if (emailInput.value.trim() !== '' && passwordInput.value.trim() !== '') {
            loginButton.removeAttribute('disabled');
            loginButton.classList.remove('disabled-button'); // Удаляем класс для неактивной кнопки
            loginButton.classList.add('login-button'); // Добавляем класс для активной кнопки
        } else {
            loginButton.setAttribute('disabled', 'true');
            loginButton.classList.add('disabled-button'); // Добавляем класс для неактивной кнопки
            loginButton.classList.remove('login-button'); // Удаляем класс для активной кнопки
        }
    }

    // Добавляем слушатели событий на оба поля ввода
    emailInput.addEventListener('input', toggleButtonState);
    passwordInput.addEventListener('input', toggleButtonState);

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



document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('id_password');
    const togglePasswordIcon = document.getElementById('toggle-password-icon');

    togglePasswordIcon.addEventListener('click', function() {
        // Переключаем тип поля ввода между "password" и "text"
        const isPassword = passwordInput.getAttribute('type') === 'password';
        passwordInput.setAttribute('type', isPassword ? 'text' : 'password');

        // Переключаем иконку
        togglePasswordIcon.setAttribute('name', isPassword ? 'eye-sharp' : 'eye-off-sharp');
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.input-group input');

    // Функция для проверки состояния полей
    function validateInputs() {
        inputs.forEach(input => {
            if (input.value.trim() === '') {
                input.classList.add('invalid');
                input.classList.remove('valid');
            } else {
                input.classList.remove('invalid');
                input.classList.add('valid');
            }
        });
    }

    // Слушатели событий для проверки полей на ввод
    inputs.forEach(input => {
        input.addEventListener('input', validateInputs);
        input.addEventListener('focus', validateInputs);
        input.addEventListener('blur', validateInputs);
    });

    // Инициализация стилей при загрузке страницы
    validateInputs();
});