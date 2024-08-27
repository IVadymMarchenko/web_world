from django.contrib import admin
from app_accounts.models import User
from app_car_moderation.models import ParkingRecord, Payment, CarList
from .utils import (
    export_users_to_csv,
    export_parking_records_to_csv,
    export_payments_to_csv,
    export_cars_to_csv,
)


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "full_name",
        "phone_number",
        "address",
        "created_at",
    )
    list_filter = ("created_at",)
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        return export_users_to_csv(queryset)

    export_to_csv.short_description = "Export selected users to CSV"


class ParkingRecordsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "license_number",
        "entry_time",
        "exit_time",
        "parking_duration",
        "parking_fee",
        "rate",
        "is_paid",
        "is_parked",
    )
    list_filter = ("entry_time", "exit_time")
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        return export_parking_records_to_csv(queryset)

    export_to_csv.short_description = "Export selected parking records to CSV"


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("parking_record", "amount", "payment_time", "is_successful")
    list_filter = ("payment_time",)
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        return export_payments_to_csv(queryset)

    export_to_csv.short_description = "Export selected payments to CSV"


class CarListAdmin(admin.ModelAdmin):
    list_display = ("license_number", "owner", "is_blacklisted", "created_at")
    search_fields = ("license_number",)
    list_filter = ("is_blacklisted", "created_at")
    ordering = ("license_number",)
    actions = ["export_to_csv"]

    def export_to_csv(self, request, queryset):
        return export_cars_to_csv(queryset)

    export_to_csv.short_description = "Export selected payments to CSV"


admin.site.register(User, UsersAdmin)
admin.site.register(ParkingRecord, ParkingRecordsAdmin)
admin.site.register(Payment, PaymentsAdmin)
admin.site.register(CarList, CarListAdmin)
