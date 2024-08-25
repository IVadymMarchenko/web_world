from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
    get_backends,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from .forms import SignUpForm, LoginForm, UserChangeForm, UserProfileForm
from .forms import BalanceTopUpForm
from app_car_moderation.models import CarList, ParkingRecord, Payment, Rate
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils.dateparse import parse_datetime
from django.urls import reverse


User = get_user_model()


def sign_up_user(request):
    if request.user.is_authenticated:
        return redirect(to="app_home:index")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user, backend=user.backend)
            return redirect(to="app_accounts:profile", username=user.username)
        else:
            return render(
                request, "app_accounts/register_form.html", context={"form": form}
            )

    form = SignUpForm()
    return render(request, "app_accounts/register_form.html", context={"form": form})


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("app_accounts:profile", username=user.username)
            else:
                messages.error(request, "Invalid email or password.")
                return redirect("app_accounts:login")
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("app_accounts:profile", username=username)
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Please enter both username and password.")
    else:
        form = LoginForm()

    return render(request, "app_accounts/login.html", {"form": form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect("app_accounts:profile", username=request.user.username)

    car_photos = user.car_images.all()

    try:
        latest_record = ParkingRecord.objects.filter(user=user, is_parked=True).latest(
            "entry_time"
        )
    except ObjectDoesNotExist:
        latest_record = None

    parking_records = ParkingRecord.objects.filter(user=user)

    return render(
        request,
        "app_accounts/profile.html",
        {
            "user": user,
            "car_photos": car_photos,
            "parking_records": parking_records,
            "latest_record": latest_record,
        },
    )


@login_required
def logout_user(request):
    logout(request)
    return redirect("app_home:index")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("app_accounts:profile", username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "app_accounts/edit_profile.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = BalanceTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            request.user.profile.balance += amount
            request.user.profile.save()
            return redirect("app_accounts:profile")  # Перенаправление после пополнения

    else:
        form = BalanceTopUpForm()

    return render(request, "app_accounts/profile.html", {"form": form})


@login_required
def top_up_balance(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount:
            try:
                amount = Decimal(amount)
                print(amount)

                if amount > 0:
                    request.user.money_balance += amount
                    request.user.save()
                    messages.success(
                        request,
                        f"Your balance has been topped up by ${amount:.2f}.",
                        extra_tags="top_balance",
                    )
                else:
                    messages.error(
                        request,
                        "The amount must be greater than zero.",
                        extra_tags="top_balance",
                    )
            except Decimal.InvalidOperation:
                messages.error(request, "Invalid amount.", extra_tags="top_balance")
        else:
            messages.error(request, "Please enter an amount.", extra_tags="top_balance")

    return redirect("app_accounts:profile", username=request.user.username)


@login_required
def parking_history(request):
    parking_records = ParkingRecord.objects.filter(user=request.user)
    return render(
        request,
        "app_accounts/parking_history.html",
        {"parking_records": parking_records, "user": request.user},
    )


def parking_view(request):
    return render(request, "app_accounts/parking.html")


@login_required
def pay_parking(request, record_id):
    parking_record = get_object_or_404(ParkingRecord, id=record_id, is_parked=True)

    # Установите время выхода
    exit_time = timezone.now()
    parking_record.process_parking_payment(exit_time)

    # Обновите баланс пользователя
    user = parking_record.user
    parking_fee = parking_record.parking_fee

    user.money_balance -= parking_fee
    user.save()

    return redirect(reverse("app_accounts:parking_history"))


# @login_required
# @csrf_exempt
# def update_balance(request):
#     if request.method == "POST":
#         user = request.user
#         data = json.loads(request.body)
#         entry_time_str = data.get("entry_Time")
#         rate_per_hour = Decimal(data.get("rate_per_hour"))

#         # Преобразование строки в объект datetime
#         entry_time = parse_datetime(entry_time_str)
#         if not entry_time:
#             return JsonResponse(
#                 {"success": False, "error": "Invalid entry time format"}
#             )

#         # Вычисляем время с момента входа
#         now = timezone.now()
#         duration_in_hours = Decimal((now - entry_time).total_seconds()) / Decimal(3600)

#         # Вычисляем сбор за парковку
#         total_fee = duration_in_hours * rate_per_hour

#         # Обновляем баланс
#         updated_balance = max(user.money_balance - total_fee, Decimal("0.00"))
#         user.money_balance = updated_balance
#         user.save()

#         return JsonResponse({"success": True, "updated_balance": str(updated_balance)})

#     return JsonResponse({"success": False, "error": "Invalid request method"})


def parking_view(request):
    rates = Rate.objects.all()
    return render(request, "app_accounts/parking.html", {"rates": rates})
