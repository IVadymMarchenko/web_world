const form = document.getElementById('loginForm');
const inputs = form.querySelectorAll('input');
const loginButton = form.querySelector('.login-button');

inputs.forEach(input => {
    input.addEventListener('input', () => {
        if ([...inputs].every(input => input.value.trim() !== '')) {
            loginButton.disabled = false;
            loginButton.classList.remove('disabled-button');
        } else {
            loginButton.disabled = true;
            loginButton.classList.add('disabled-button');
        }
    });
});