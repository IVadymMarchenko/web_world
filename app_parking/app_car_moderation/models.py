from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    is_blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.license_plate} ({self.owner.username})"


class ParkingRecord(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="parking_records"
    )
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(blank=True, null=True)
    parking_duration = models.DurationField(blank=True, null=True)
    parking_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)

    def calculate_duration_and_fee(self, rate_per_hour):
        if self.exit_time:
            self.parking_duration = self.exit_time - self.entry_time
            hours_parked = self.parking_duration.total_seconds() / 3600
            self.parking_fee = round(hours_parked * rate_per_hour, 2)
            self.save()

    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.entry_time.strftime('%Y-%m-%d %H:%M:%S')}"
