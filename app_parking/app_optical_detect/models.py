from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Image(models.Model):
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="images"
    )
    image_file = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image uploaded by {self.uploaded_by.username} on {self.uploaded_at}"


class LicensePlateDetection(models.Model):
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="plate_detections"
    )
    detected_plate = models.CharField(max_length=20)
    detected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Plate detected: {self.detected_plate} in image {self.image.id} at {self.detected_at}"
