from django.contrib import admin
from django import forms
from .models import Report
from django.utils import timezone
from django.contrib import messages
from django.core.management import call_command
import csv
from django.http import HttpResponse

@admin.action(description="Export selected reports to CSV")
def export_as_csv(modeladmin, request, queryset):
    

    meta = queryset.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["report_type", "generated_at", "file_path"]
    actions = ["generate_report"]

    def generate_report(self, request, queryset):
        for report in queryset:
            try:
                call_command(
                    "generate_report",
                    report_type=report.report_type,
                    start_date=request.POST.get("start_date"),
                    end_date=request.POST.get("end_date"),
                )
                messages.success(
                    request, f"Report for {report.report_type} generated successfully."
                )
            except Exception as e:
                messages.error(request, f"Error generating report: {str(e)}")

    generate_report.short_description = "Generate selected reports"

    def get_changelist_form(self, request, **kwargs):
        return ReportAdminForm


class ReportAdminForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}), required=False
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = Report
        fields = ["start_date", "end_date", "report_type"]
