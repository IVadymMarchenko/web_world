from django.db import models
from app_car_moderation.models import ParkingRecord


class Rate(models.Model):
    rate_name = models.CharField(max_length=50)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.rate_name} - {self.rate_per_hour} per hour"


class Payment(models.Model):
    parking_record = models.ForeignKey(
        ParkingRecord, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_time = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Payment for {self.parking_record} - {self.amount} at {self.payment_time}"
        )
