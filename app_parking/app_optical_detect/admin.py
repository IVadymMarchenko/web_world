from django.contrib import admin
from .models import Image, LicensePlateDetection


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("uploaded_by", "image_file", "uploaded_at")
    search_fields = ("uploaded_by__username",)
    list_filter = ("uploaded_at",)


@admin.register(LicensePlateDetection)
class LicensePlateDetectionAdmin(admin.ModelAdmin):
    list_display = ("image", "detected_plate", "detected_at")
    search_fields = ("detected_plate", "image__uploaded_by__username")
    list_filter = ("detected_at",)
