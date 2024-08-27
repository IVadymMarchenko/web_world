from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

from django.utils import timezone

User = get_user_model()


class Car_Image(models.Model):
    number_car = models.CharField(max_length=500, null=True)
    model = models.CharField(max_length=25, null=True)
    year = models.CharField(max_length=6, null=True)
    image = models.FileField(upload_to="photo_for_users", max_length=500)
    detected_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="car_images")
