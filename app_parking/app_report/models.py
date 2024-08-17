from django.db import models
from django.utils import timezone


class Report(models.Model):
    REPORT_TYPES = [
        ("parking", "Parking Report"),
        ("payment", "Payment Report"),
        ("user", "User Report"),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(default=timezone.now)
    file_path = models.FileField(upload_to="reports/")

    def __str__(self):
        return f"{self.get_report_type_display()} generated at {self.generated_at}"
