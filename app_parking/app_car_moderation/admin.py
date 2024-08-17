from django.contrib import admin
from .models import Vehicle, ParkingRecord


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("license_plate", "owner", "is_blacklisted")
    search_fields = ("license_plate", "owner__username")
    list_filter = ("is_blacklisted",)


@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle",
        "entry_time",
        "exit_time",
        "parking_duration",
        "parking_fee",
        "is_paid",
    )
    search_fields = ("vehicle__license_plate",)
    list_filter = ("is_paid", "entry_time")
