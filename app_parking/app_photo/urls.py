from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'app_photo'

urlpatterns = [
    path('profile/', views.upload, name='upload'),
    path('profile_avatar/', views.upload_avatar, name='upload_avatar')
]