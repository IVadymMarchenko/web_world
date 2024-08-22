from django.urls import path,include
from . import views


app_name = 'app_home'

urlpatterns = [
    path('', views.home, name='home'),
    #path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('edit-profile/', views.edit_profile, name='edit_profile')
]