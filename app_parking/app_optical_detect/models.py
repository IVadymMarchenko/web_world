from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class LicenseNumberDetection(models.Model):

    image_file = models.ImageField(upload_to="images/")
    detected_number = models.CharField(max_length=20)
    detected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Plate detected: {self.detected_number}"
