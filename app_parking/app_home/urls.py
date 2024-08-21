from django.urls import path
from . import views


app_name = "app_home"

urlpatterns = [
    path("", views.home, name="index"),
    path("about_project/", views.about_us_detail, name="about_project"),
]
