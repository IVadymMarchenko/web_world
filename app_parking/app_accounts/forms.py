from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label="Email", widget=forms.EmailInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'full_name', 'phone_number', 'address', 'license_number']

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
        fields = ['full_name', 'email', 'phone_number', 'address', 'license_number', 'location', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }