from symtable import Class

from django.shortcuts import render, redirect
from .forms import FormPicture
from .models import Car_Image
from .read_car_number import CarPlateRecognizer
import cloudinary.uploader
import os
from django.http import HttpResponseRedirect
import sys
# Define the path to your Haar cascade file
# dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
cascade_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "model/haarcascade_russian_plate_number.xml"))
print(cascade_path)
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




