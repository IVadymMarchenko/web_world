from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, UserChangeForm, UserProfileForm
from django.contrib.auth import logout
from django.contrib import messages
# from .forms import EditProfileForm
from django.contrib.auth import get_user_model

from django.views import View
from .models import ParkingHistory
User = get_user_model()
def sign_up_user(request):
    if request.user.is_authenticated:
        return redirect(to="app_home:index")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="app_accounts:profile")
        else:
            return render(request, "app_accounts/register_form.html", context={"form": form})

    form = SignUpForm()
    return render(request, "app_accounts/register_form.html", context={"form": form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app_home:index') 
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')
    else:
        form = LoginForm()
    return render(request, 'app_accounts/login.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect('app_accounts:profile', username=request.user.username)
    return render(request, 'app_accounts/profile.html', {'user': user})

@login_required
def logout_user(request):
    logout(request)
    return redirect('app_home:index')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('app_accounts:profile', username=request.user.username) 
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'app_accounts/edit_profile.html', {'form': form})



@login_required
def profile_view(request):
    user = request.user
    parking_history = user.parking_history.all()

    context = {
        'user': user,
        'parking_history': parking_history,
    }
    return render(request, 'app_accounts/profile.html', context)

class ParkingHistoryView(View):
    def get(self, request):
        parking_records = ParkingHistory.objects.filter(user=request.user)
        return render(request, 'app_accounts/parking_history.html', {'parking_records': parking_records})
    
def pay_parking(request, pk):
    parking_record = get_object_or_404(ParkingHistory, pk=pk, user=request.user)
    parking_record.is_paid = True
    parking_record.save()
    return redirect('parking_history')