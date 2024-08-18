from django.contrib import admin
from .models import LicenseNumberDetection


class LicenseNumberDetectionAdmin(admin.ModelAdmin):
    list_display = ("detected_number", "detected_at", "image_file")
    search_fields = ("detected_number",)
    list_filter = ("detected_at",)
    readonly_fields = ("detected_at",)
    ordering = ("-detected_at",)


admin.site.register(LicenseNumberDetection, LicenseNumberDetectionAdmin)
