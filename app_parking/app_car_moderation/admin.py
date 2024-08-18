from django.contrib import admin
from .models import Rate, CarList, ParkingRecord, Payment


class RateAdmin(admin.ModelAdmin):
    list_display = ("rate_name", "rate_per_hour")
    search_fields = ("rate_name",)
    ordering = ("rate_name",)


class CarListAdmin(admin.ModelAdmin):
    list_display = ("license_number", "owner", "is_blacklisted")
    search_fields = ("license_number",)
    list_filter = ("is_blacklisted",)
    ordering = ("license_number",)


class ParkingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "entry_time",
        "exit_time",
        "parking_duration",
        "parking_fee",
        "rate",
        "is_paid",
        "is_parked",
    )
    search_fields = ("user__username", "user__email")
    list_filter = ("is_paid", "is_parked", "rate")
    readonly_fields = ("parking_duration", "parking_fee")
    ordering = ("-entry_time",)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("parking_record", "amount", "payment_time", "is_successful")
    search_fields = ("parking_record__user__username", "amount")
    list_filter = ("is_successful",)
    ordering = ("-payment_time",)


admin.site.register(Rate, RateAdmin)
admin.site.register(CarList, CarListAdmin)
admin.site.register(ParkingRecord, ParkingRecordAdmin)
admin.site.register(Payment, PaymentAdmin)
