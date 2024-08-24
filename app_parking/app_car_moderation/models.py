from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from decimal import Decimal

User = get_user_model()


class Rate(models.Model):
    RATE_CHOICES = [
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("standard", "Standard"),
    ]

    rate_name = models.CharField(max_length=50, choices=RATE_CHOICES)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.rate_name} - {self.rate_per_hour}"


@receiver(post_migrate)
def create_default_rates(sender, **kwargs):
    if sender.name == "app_car_moderation":
        Rate.objects.get_or_create(rate_name="basic", defaults={"rate_per_hour": 10.00})
        Rate.objects.get_or_create(
            rate_name="premium", defaults={"rate_per_hour": 30.00}
        )
        Rate.objects.get_or_create(
            rate_name="standard", defaults={"rate_per_hour": 20.00}
        )


class CarList(models.Model):
    license_number = models.CharField(max_length=15, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    is_blacklisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.license_number} ({self.owner.username})"

    @classmethod
    def search_by_license_number(cls, license_number):
        try:
            return cls.objects.get(license_number=license_number)
        except cls.DoesNotExist:
            return None


class ParkingRecord(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="parking_records"
    )
    license_number = models.CharField(max_length=15)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(blank=True, null=True)
    parking_duration = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    parking_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    rate = models.ForeignKey(
        Rate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parking_records",
        default=1,
    )
    is_paid = models.BooleanField(default=False)
    is_parked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.rate:
            try:
                self.rate = Rate.objects.get(rate_name="basic")
            except Rate.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def calculate_duration_and_fee(self):
        if self.exit_time is None:
            self.exit_time = timezone.now()

        # Расчет продолжительности парковки
        parking_duration = round(
            Decimal((self.exit_time - self.entry_time).total_seconds()), 2
        )
        if parking_duration is None:
            raise ValueError("Parking duration is not set correctly.")

        hours_parked = round(parking_duration / Decimal(3600), 2)

        if self.rate:
            parking_fee = round(hours_parked * self.rate.rate_per_hour, 2)
        else:
            parking_fee = None
        print(parking_duration)
        print(hours_parked)
        print(self.exit_time)
        print(self.entry_time)
        print(parking_fee)

        return {
            "parking_duration": parking_duration,
            "parking_fee": parking_fee,
            "hours_parked": hours_parked,
        }

    def process_parking_payment(self, exit_time):
        self.exit_time = exit_time
        data = self.calculate_duration_and_fee()
        self.parking_duration = data["hours_parked"]
        self.parking_fee = data["parking_fee"]
        self.is_paid = True
        self.is_parked = False
        self.save()

        # Создание записи оплаты
        Payment.objects.create(
            parking_record=self, amount=self.parking_fee, is_successful=True
        )

        return data

    def __str__(self):
        return f"{self.user.username} - {self.entry_time.strftime('%Y-%m-%d %H:%M:%S')}"


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
