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
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from app_car_moderation.models import CarList, ParkingRecord
from dotenv import load_dotenv

cascade_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "model/haarcascade_russian_plate_number.xml"))

User = get_user_model()


# Define the path to your Haar cascade file
cascade_path = os.path.join(
    os.path.dirname(__file__), "model/haarcascade_russian_plate_number.xml"
)


# Initialize your recognizer with the correct path
recognizer = CarPlateRecognizer(
    classifier_path=cascade_path, font_path="font/simfang.ttf"
)


def send_blacklist_notification(user, license_number):

    subject = f"Dear {user.full_name} - your Car is Blacklisted"
    message = f"""
    Dear {user.username},

    We have detected that your car with license number {license_number} is in the blacklist due to unpaid parking fees.
    
    Please contact our support team to resolve this issue.

    Thank you,
    WEB_WORLD: PARK-AUTO
    """
    from_email = os.getenv("EMAIL_HOST_USER")
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def save_to_car_list(request, recognized_number, user):
    try:

        car_list_entry = CarList.objects.get(
            license_number=recognized_number, owner=user
        )
        if car_list_entry.is_blacklisted:
            send_blacklist_notification(user, recognized_number)
            messages.error(
                request,
                f"Car with license number {recognized_number} is Blacklisted.",
            )

        return car_list_entry
    except ObjectDoesNotExist:
        car_list_entry = CarList(license_number=recognized_number, owner=user)
        car_list_entry.save()
        return car_list_entry


def save_to_parking_record(request, user, recognized_number):
    if ParkingRecord.objects.filter(user=user, is_parked=True).exists():
        messages.warning(
            request,
            f"Car with license number {recognized_number} is already parked.",
        )

        return None

    # If no active parking record exists, create a new one
    parking_record = ParkingRecord(
        user=user, license_number=recognized_number, is_parked=True
    )
    parking_record.save()
    return parking_record


def handle_file_upload(file):
    """Processes a file upload and returns a secure_url."""
    uploader_file = cloudinary.uploader.upload(file, resource_type="raw")
    return uploader_file["secure_url"]


def recognize_numer_car(image_url):
    """Recognizes a car number from an image."""
    cars_number = recognizer.recognize(image_url) or None
    return cars_number


def save_car_data(request, recognized_number, user, image_url):
    """Saves vehicle data to the database."""
    if Car_Image.objects.filter(number_car=recognized_number, user=user).exists():
        messages.error(
            request,
            f"Such image with {recognized_number} recognized text is already present.",
        )
        return None

    Car_Image.objects.create(number_car=recognized_number, user=user, image=image_url)
    print(f"Saved car number: {recognized_number}")


def upload(request):
    """Upload a file to the database."""
    car_numbers = []  # Инициализация списка номеров

    if request.method == "POST":
        form = FormPicture(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get("image")
            if file:
                secure_url = handle_file_upload(file)
                recognized_numbers = recognize_numer_car(secure_url)
                if recognized_numbers:

                    user = request.user
                    car_list_entry = save_to_car_list(
                        request, recognized_numbers[0], user
                    )

                    if car_list_entry and not car_list_entry.is_blacklisted:

                        license_number = car_list_entry.license_number
                        existing_record = ParkingRecord.objects.filter(
                            user=user, license_number=license_number, is_parked=True
                        ).exists()

                        if not existing_record:
                            save_to_parking_record(request, user, recognized_numbers)
                            save_car_data(
                                request, recognized_numbers[0], user, secure_url
                            )

                    car_numbers = recognized_numbers  # Сохраняем распознанные номера

                # Сохраняем распознанные номера в сессию
                request.session["car_numbers"] = car_numbers
                # Перенаправляем на ту же страницу после обработки POST-запроса
                return HttpResponseRedirect(request.path_info)
    else:

        form = FormPicture()

        # Получаем распознанные номера из сессии, если они есть
        car_numbers = request.session.get("car_numbers", [])

    car_photos = Car_Image.objects.all()

    # Передаем форму, фото и распознанные номера в шаблон
    return render(
        request,
        "app_accounts/parking.html",
        {"form": form, "car_photos": car_photos, "car_numbers": car_numbers},
    )


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

