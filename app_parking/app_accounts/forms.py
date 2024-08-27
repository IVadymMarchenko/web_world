from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms


from .models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'autofocus': True
        }),
        required=True,
        min_length=5,
        max_length=20
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}),
        required=True
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'required': True,
            'pattern': '[a-z0-9.]+@[a-z0-9.]+\.[a-z]{2,}$'
        })
    )
    full_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
        required=True,
        min_length=2,
        max_length=50
    )
    phone_number = forms.CharField(
        label="Phone Number",
        validators=[
            RegexValidator(
                regex=r'^(\+?380|0)[4-9][0-9]\d{7}$',
                message="Please enter a valid phone number. Format: +380981231212 or 0981231223"
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your phone number',
            'pattern': r'^(\+?380|0)[4-9][0-9]\d{7}$'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "full_name",
            "phone_number",
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not 5 <= len(username) <= 20:
            raise ValidationError("Username must be between 5 and 20 characters.")
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not 2 <= len(full_name) <= 50:
            raise ValidationError("Full Name must be between 2 and 50 characters.")
        if any(char.isdigit() or not char.isalpha() and char != ' ' for char in full_name):
            raise ValidationError("Full Name can only contain letters and spaces.")
        return full_name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone_number",
            "address",
            "birth_date",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }


class BalanceTopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Amount to top up")
