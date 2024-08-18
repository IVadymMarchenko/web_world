from django.urls import path
from .views import search_car

app_name = "app_car_moderation"

urlpatterns = [
    path("search/", search_car, name="search_car"),
]
