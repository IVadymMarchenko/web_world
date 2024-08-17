from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("report_type", "generated_at", "file_path")
    search_fields = ("report_type",)
    list_filter = ("report_type", "generated_at")
    readonly_fields = (
        "file_path",
    )  # Зробити поле файлу тільки для читання, якщо ви не хочете, щоб його змінювали

    def has_change_permission(self, request, obj=None):
        # Вимкнути можливість редагування звітів, якщо це необхідно
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)
