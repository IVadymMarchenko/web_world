document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[type="password"], input[type="text"], input[type="email"]');

    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (input.value.trim() !== '') {
                input.classList.add('filled');
                input.classList.remove('empty');
            } else {
                input.classList.add('empty');
                input.classList.remove('filled');
            }
        });

        // Устанавливаем начальный класс в зависимости от текущего значения
        if (input.value.trim() !== '') {
            input.classList.add('filled');
        } else {
            input.classList.add('empty');
        }
    });
});