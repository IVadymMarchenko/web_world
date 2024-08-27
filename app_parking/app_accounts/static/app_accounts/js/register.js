document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registration-form');
    
    if (!form) return; // Проверяем, существует ли форма

    const registerButton = form.querySelector('button[type="submit"]');

    form.addEventListener('input', function () {
        // Проверяем, заполнены ли все обязательные поля
        const allFilled = [...form.querySelectorAll('input[required]')].every(input => input.value.trim() !== '');
        registerButton.disabled = !allFilled;

        // Меняем цвет кнопки в зависимости от состояния
        if (allFilled) {
            registerButton.classList.remove('disabled');
        } else {
            registerButton.classList.add('disabled');
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registration-form');
    const inputs = form.querySelectorAll('input');

    inputs.forEach(input => {
        input.addEventListener('input', function () {
            if (input.validity.valid) {
                input.style.borderColor = '#28a745'; // Зеленый, если поле заполнено верно
            } else {
                if (input.value !== '') {
                    input.style.borderColor = '#dc3545'; // Красный, если заполнено неверно
                }
            }
        });

        input.addEventListener('blur', function () {
            if (!input.value) {
                input.style.borderColor = ''; // Сброс цвета, если поле пустое
            }
        });
    });
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


document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение отправки формы
    
    let formIsValid = true;

    // Проверяем каждое поле ввода
    document.querySelectorAll('.input-group').forEach(function(group) {
        const input = group.querySelector('input');
        const validIcon = group.querySelector('.valid-icon');
        const invalidIcon = group.querySelector('.invalid-icon');
        
        if (input.value.trim() === '' || input.classList.contains('error')) {
            group.classList.add('invalid');
            group.classList.remove('valid');
            invalidIcon.style.display = 'block';
            validIcon.style.display = 'none';
            formIsValid = false;
        } else {
            group.classList.add('valid');
            group.classList.remove('invalid');
            invalidIcon.style.display = 'none';
            validIcon.style.display = 'block';
        }
    });

    // Если форма валидна, отправляем ее
    if (formIsValid) {
        this.submit();  // Отправляем форму
    }
});

// Иконки будут оставаться до следующей проверки, не исчезая после первой попытки
document.querySelectorAll('.input-group input').forEach(function(input) {
    input.addEventListener('input', function() {
        const group = input.closest('.input-group');
        const validIcon = group.querySelector('.valid-icon');
        const invalidIcon = group.querySelector('.invalid-icon');

        if (input.value.trim() !== '') {
            group.classList.add('valid');
            group.classList.remove('invalid');
            invalidIcon.style.display = 'none';
            validIcon.style.display = 'block';
        } else {
            group.classList.add('invalid');
            group.classList.remove('valid');
            validIcon.style.display = 'none';
            invalidIcon.style.display = 'block';
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('{{ form.password1.id_for_label }}');
    const confirmPasswordInput = document.getElementById('{{ form.password2.id_for_label }}');

    function checkPasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength += 1;
        if (password.match(/[a-z]+/)) strength += 1;
        if (password.match(/[A-Z]+/)) strength += 1;
        if (password.match(/[0-9]+/)) strength += 1;
        if (password.match(/[$@#&!]+/)) strength += 1;
        return strength;
    }

    passwordInput.addEventListener('input', function () {
        const strength = checkPasswordStrength(passwordInput.value);
        const confirmPassword = confirmPasswordInput.value;

        // Подсветка на основе надежности пароля
        if (strength <= 2) {
            passwordInput.style.borderColor = '#dc3545'; // Красный
        } else if (strength === 3) {
            passwordInput.style.borderColor = '#ffc107'; // Желтый
        } else if (strength >= 4) {
            passwordInput.style.borderColor = '#28a745'; // Зеленый
        }

        // Проверка совпадения паролей
        if (confirmPassword !== '' && confirmPassword !== passwordInput.value) {
            confirmPasswordInput.style.borderColor = '#dc3545'; // Красный, если пароли не совпадают
        } else {
            confirmPasswordInput.style.borderColor = '#28a745'; // Зеленый, если пароли совпадают
        }
    });

    confirmPasswordInput.addEventListener('input', function () {
        const confirmPassword = confirmPasswordInput.value;

        if (confirmPassword !== passwordInput.value) {
            confirmPasswordInput.style.borderColor = '#dc3545'; // Красный, если пароли не совпадают
        } else {
            confirmPasswordInput.style.borderColor = '#28a745'; // Зеленый, если пароли совпадают
        }
    });
});
