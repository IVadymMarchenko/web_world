from django.contrib import admin
from .models import Rate, Payment


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("rate_name", "rate_per_hour")
    search_fields = ("rate_name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("parking_record", "amount", "payment_time", "is_successful")
    search_fields = ("parking_record__vehicle__license_plate", "amount")
    list_filter = ("is_successful", "payment_time")
