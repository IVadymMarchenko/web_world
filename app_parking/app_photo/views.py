from symtable import Class

from django.shortcuts import render, redirect
from .forms import FormPicture
from .models import Car_Image
from .forms import AvatarForm
from .read_car_number import CarPlateRecognizer
import cloudinary.uploader
import os
from django.http import HttpResponseRedirect
from app_accounts.models import User,Profile

# Define the path to your Haar cascade file
cascade_path = os.path.join(os.path.dirname(__file__), 'model/haarcascade_russian_plate_number.xml')

# Initialize your recognizer with the correct path
recognizer = CarPlateRecognizer(classifier_path=cascade_path, font_path='font/simfang.ttf')


def handle_file_upload(file):
    """Processes a file upload and returns a secure_url."""
    uploader_file = cloudinary.uploader.upload(file,resource_type='raw')
    return uploader_file['secure_url']


def recognize_numer_car(image_url):
    """Recognizes a car number from an image."""
    cars_number=recognizer.recognize(image_url) or None
    return cars_number

def save_car_data(car_number,image_url):
    """Saves vehicle data to the database."""
    Car_Image.objects.create(number_car=car_number,image=image_url)
    print(f"Saved car number: {car_number}")



def upload(request):
    """Upload a file to the database."""
    car_numbers = []  # Инициализация списка номеров

    if request.method == 'POST':
        form = FormPicture(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('image')
            if file:
                secure_url = handle_file_upload(file)
                recognized_numbers = recognize_numer_car(secure_url)
                if recognized_numbers:

                    save_car_data(recognized_numbers[0], secure_url)
                    car_numbers = recognized_numbers  # Сохраняем распознанные номера

                # Сохраняем распознанные номера в сессию
                request.session['car_numbers'] = car_numbers
                # Перенаправляем на ту же страницу после обработки POST-запроса
                return HttpResponseRedirect(request.path_info)
    else:
        form = FormPicture()

        # Получаем распознанные номера из сессии, если они есть
        car_numbers = request.session.get('car_numbers', [])

    car_photos =Car_Image.objects.all()

    # Передаем форму, фото и распознанные номера в шаблон
    return render(request, 'app_accounts/profile.html', {
        'form': form,
        'car_photos': car_photos,
        'car_numbers': car_numbers
    })


def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('avatar')
            if file:
                # Загрузка файла на Cloudinary
                uploaded_file = cloudinary.uploader.upload(file, resource_type="image")  # image for images uploaded

                # Получение объекта Profile для текущего пользователя
                user_profile = Profile.objects.get(user=request.user)
                user_profile.avatar = uploaded_file['secure_url']
                user_profile.save()

                # Сообщение об успешной загрузке
                form.add_error(None, 'Аватар успешно загружен.')

                return redirect('app_photo:upload')
    else:
        form = AvatarForm()

    return render(request, 'app_accounts/profile.html', {'form': form})


