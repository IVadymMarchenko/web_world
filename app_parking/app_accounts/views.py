from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model,
    get_backends,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from .forms import (
    SignUpForm,
    LoginForm,
    UserChangeForm,
    UserProfileForm,
    PasswordChangeForm,
)
from .forms import BalanceTopUpForm
from app_car_moderation.models import CarList, ParkingRecord, Payment, Rate
from app_photo.models import Car_Image
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils.dateparse import parse_datetime
from django.urls import reverse

from .models import Profile
from app_car_moderation.models import ParkingRecord
from urllib.parse import unquote
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

            username = user.username
            messages.success(
                request,
                f"Welcome, {username}!<br>Registration successful! Redirecting to your profile...",
            )

            return render(
                request,
                "app_accounts/register_form.html",
                context={
                    "form": form,
                    "redirect": True,
                    "redirect_url": reverse(
                        "app_accounts:profile", kwargs={"username": username}
                    ),
                },
            )

        else:
            messages.error(
                request, "There was an error with your registration. Please try again."
            )
            return render(
                request, "app_accounts/register_form.html", context={"form": form}
            )
    else:
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




def format_duration(duration):
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

from urllib.parse import unquote

@login_required
def profile(request, username):

    user = get_object_or_404(User, username=username)
    user_profile_avatar = get_object_or_404(Profile, user=user)


    if user != request.user:
        return redirect("app_accounts:profile", username=request.user.username)


    last_parking_session = (
        ParkingRecord.objects.filter(user=user, exit_time__isnull=False)
        .order_by('-exit_time')
        .first()
    )
    last_parking_text = last_parking_session.exit_time.strftime('%Y-%m-%d %H:%M:%S') if last_parking_session else "No recent activity."


    membership_since = user.date_joined.strftime('%B %Y')
    total_parkings = ParkingRecord.objects.filter(user=user).count()


    current_parking = ParkingRecord.objects.filter(user=user, is_parked=True).first()
    current_parking_info = None
    parked_car_photo_url = None

    if current_parking:

        duration = timezone.now() - current_parking.entry_time
        formatted_duration = format_duration(duration)

        current_parking_info = {
            'license_number': current_parking.license_number,
            'rate_name': current_parking.rate.rate_name if current_parking.rate else "Unknown",
            'entry_time': current_parking.entry_time.strftime('%Y-%m-%d %H:%M:%S'),
            'hours_parked': formatted_duration,
            'status': "On Parking",
        }

        parked_car_photo = Car_Image.objects.filter(
            number_car=current_parking.license_number, user=user
        ).order_by('-detected_at').first()


        if parked_car_photo and parked_car_photo.image:
            image_url = parked_car_photo.image.url
            

            fixed_url = unquote(image_url)


            if fixed_url.startswith('/https:'):
                fixed_url = fixed_url[1:] 
            
            parked_car_photo_url = fixed_url
            print(f"Окончательно исправленный URL: {parked_car_photo_url}")


    context = {
        "user": user,
        "user_profile_avatar": user_profile_avatar,
        "parking_records": ParkingRecord.objects.filter(user=user),
        "latest_record": current_parking_info,
        'last_parking_text': last_parking_text,
        'membership_since': membership_since,
        'total_parkings': total_parkings,
        'parked_car_photo_url': parked_car_photo_url,  
    }

    return render(request, "app_accounts/profile.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect("app_home:index")


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile_avatar = get_object_or_404(Profile, user=user)

    active_tab = request.GET.get("tab", "account-general")

    form = UserProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == "POST":
        if "save_profile" in request.POST:
            form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                print("Form is valid. Saving data...")
                form.save()
                messages.success(
                    request, "Profile updated successfully.", extra_tags="edit_profile"
                )
                return redirect("app_accounts:profile", username=request.user.username)
            else:
                print("Form is not valid:", form.errors)
                messages.error(
                    request,
                    "Please correct the errors below.",
                    extra_tags="edit_profile",
                )
            active_tab = "account-general"

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request,
                    "Your password was successfully changed.",
                    extra_tags="edit_profile",
                )
                return redirect(
                    "app_accounts:edit_profile", username=request.user.username
                )
            else:
                messages.error(
                    request,
                    "Please correct the errors below.",
                    extra_tags="edit_profile",
                )
            active_tab = "account-change-password"

    return render(
        request,
        "app_accounts/edit_profile.html",
        {
            "form": form,
            "password_form": password_form,
            "user_profile_avatar": user_profile_avatar,
            "active_tab": active_tab,
        },
    )




@login_required
def profile_view(request):
    if request.method == "POST":
        form = BalanceTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            request.user.profile.balance += amount
            request.user.profile.save()
            return redirect("app_accounts:profile") 

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



@login_required
def pay_parking(request, record_id):
    parking_record = get_object_or_404(ParkingRecord, id=record_id, is_parked=True)

    exit_time = timezone.now()
    parking_record.process_parking_payment(exit_time)

    user = parking_record.user
    parking_fee = parking_record.parking_fee

    user.money_balance -= parking_fee
    user.save()

    return redirect(reverse("app_accounts:parking_history"))


@login_required
def parking_view(request):
    rates = Rate.objects.all()
    return render(request, "app_accounts/parking.html", {"rates": rates})
