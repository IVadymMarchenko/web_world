document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('car-photo-upload');
    const saveButton = document.querySelector('.upload-button');
    const pricingOptions = document.querySelector('.pricing-options');
    const rateInputs = document.querySelectorAll('input[name="rate"]');

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
                // Отключить кнопку "Save" до выбора тарифа
                saveButton.disabled = true;
            };
            reader.readAsDataURL(file);
        }
    });

    rateInputs.forEach(function (rateInput) {
        rateInput.addEventListener('change', function () {
            // Включить кнопку "Save" после выбора тарифа
            saveButton.disabled = false;
        });
    });
});
