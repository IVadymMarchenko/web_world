from symtable import Class

from django.shortcuts import render, redirect
from .forms import FormPicture
from .models import Car_Image
from .forms import AvatarForm
from .read_car_number import CarPlateRecognizer
import cloudinary.uploader
import os
from django.http import HttpResponseRedirect
from app_accounts.models import User, Profile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from app_car_moderation.models import CarList, ParkingRecord, Rate
from dotenv import load_dotenv


cascade_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "model/haarcascade_russian_plate_number.xml"
    )
)

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

    We have detected that your tried to park car with registration number {license_number} but unsuccessful.
    Due to reason that your profile balance below zero and equal {user.money_balance} $.
    Please pay for continue parking.
    
    Please contact our support team to resolve this issue.

    Thank you,
    WEB_WORLD: PARK-AUTO
    """
    from_email = os.getenv("EMAIL_HOST_USER")
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def save_to_car_list(request, recognized_number, user):
    try:
        car_list_entry = CarList.objects.get(license_number=recognized_number)

        if car_list_entry.owner != user:
            messages.error(
                request,
                f"Car with license number {recognized_number} is already associated with another user.",
                extra_tags="if_parking",
            )
            return None

        if car_list_entry.is_blacklisted:
            send_blacklist_notification(user, recognized_number)
            messages.error(
                request,
                f"Car with license number {recognized_number} is Blacklisted.",
                extra_tags="if_parking",
            )

        return car_list_entry

    except CarList.DoesNotExist:
        car_list_entry = CarList(license_number=recognized_number, owner=user)
        car_list_entry.save()
        return car_list_entry


def save_to_parking_record(request, user, recognized_number, rate_record):
    if ParkingRecord.objects.filter(
        user=user, license_number=recognized_number, is_parked=True
    ).exists():
        messages.warning(
            request,
            f"Car with license number {recognized_number} is already parked.",
            extra_tags="if_parking",
        )

        return None

    # If no active parking record exists, create a new one
    parking_record = ParkingRecord(
        user=user, license_number=recognized_number, is_parked=True, rate=rate_record
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
        # messages.error(
        #     request,
        #     f"Such image with {recognized_number} recognized text is already present.",
        # )
        return None

    Car_Image.objects.create(number_car=recognized_number, user=user, image=image_url)
    print(f"Saved car number: {recognized_number}")


def upload(request):
    """Upload a file to the database."""
    rates = Rate.objects.all()
    car_numbers = []
    if request.method == "POST":
        form = FormPicture(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get("image")
            if file:
                secure_url = handle_file_upload(file)
                recognized_numbers = recognize_numer_car(secure_url)

                if recognized_numbers:
                    cleaned_list = [rec.replace(" ", "") for rec in recognized_numbers]
                    recognized_numbers = cleaned_list
                    user = request.user
                    car_list_entry = save_to_car_list(
                        request, recognized_numbers[0], user
                    )

                    if (
                        car_list_entry
                        and not car_list_entry.is_blacklisted
                        and user.money_balance >= 0
                    ):

                        # license_number = car_list_entry.license_number
                        # existing_record = ParkingRecord.objects.filter(
                        #     user=user, license_number=license_number, is_parked=True
                        # ).exists()

                        # if not existing_record:
                        id_value = int(request.POST.get("rate"))
                        rate_record = Rate.objects.get(id=id_value)
                        save_to_parking_record(
                            request, user, recognized_numbers[0], rate_record
                        )
                        save_car_data(request, recognized_numbers[0], user, secure_url)
                        messages.success(
                            request,
                            f"Recognized car number is  {recognized_numbers[0]}.",
                            extra_tags="if_parking",
                        )

                    elif user.money_balance < 0:
                        send_blacklist_notification(user, recognized_numbers)
                        messages.error(
                            request,
                            f"Your balance below zero. Please ",
                            extra_tags="if_parking",
                        )

                    car_numbers = recognized_numbers  # Сохраняем распознанные номера
                else:
                    messages.warning(
                        request,
                        f"Nothing to recognize. Please try again.",
                        extra_tags="if_parking",
                    )

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
        {
            "form": form,
            "car_photos": car_photos,
            "car_numbers": car_numbers,
            "rates": rates,
        },
    )


def upload_avatar(request):

    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get("profile_image")

            if file:
                # Загрузка файла на Cloudinary
                uploaded_file = cloudinary.uploader.upload(
                    file, resource_type="image"
                )  # image for images uploaded
                # Получение объекта Profile для текущего пользователя
                user_profile = Profile.objects.get(user=request.user)
                user_profile.avatar = uploaded_file["secure_url"]
                user_profile.save()

                # Сообщение об успешной загрузке
                # form.add_error(None, "Аватар успешно загружен.")

                return redirect(
                    "app_accounts:edit_profile", username=request.user.username
                )
    else:
        form = AvatarForm()

    return redirect("app_accounts:edit_profile", username=request.user.username)
