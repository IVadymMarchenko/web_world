document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('car-photo-upload');
    const okButton = document.getElementById('ok-button');
    const pricingOptions = document.querySelector('.pricing-options');
    const saveButton = document.querySelector('.upload-button');

    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
            // Отобразить фото
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('uploaded-car-photo');
                const uploadedPhotosContainer = document.getElementById('uploaded-car-photos');
                uploadedPhotosContainer.innerHTML = ''; // Очистить контейнер перед добавлением нового фото
                uploadedPhotosContainer.appendChild(img);
                // Показать чекбоксы
                pricingOptions.style.display = 'block';
                // Показать кнопку "OK"
                okButton.style.display = 'block';
                // Отключить кнопку "Save" до выбора тарифа
                saveButton.disabled = true;
            };
            reader.readAsDataURL(file);
        }
    });

    okButton.addEventListener('click', function () {
        // Проверить, выбран ли тариф
        const selectedRate = document.querySelector('input[name="rate"]:checked');
        if (selectedRate) {
            // Включить кнопку "Save"
            saveButton.disabled = false;
            // Скрыть кнопку "OK"
            okButton.style.display = 'none';
        } else {
            alert('Please select a parking rate.');
        }
    });
});
