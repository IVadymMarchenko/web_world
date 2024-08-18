import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from app_report.models import Report
from app_car_moderation.models import ParkingRecord, Payment, User
from django.core.files.base import ContentFile
from io import StringIO


class Command(BaseCommand):
    help = "Generate a report and save it as a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "report_type",
            choices=["parking", "payment", "user"],
            help="Type of report to generate",
        )
        parser.add_argument(
            "--start_date", type=str, help="Start date in format YYYY-MM-DD"
        )
        parser.add_argument(
            "--end_date", type=str, help="End date in format YYYY-MM-DD"
        )

    def handle(self, *args, **kwargs):
        report_type = kwargs["report_type"]
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")

        if start_date:
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d")

        if report_type == "parking":
            queryset = ParkingRecord.objects.all()
            if start_date:
                queryset = queryset.filter(entry_time__gte=start_date)
            if end_date:
                queryset = queryset.filter(exit_time__lte=end_date)

            header = [
                "User",
                "License Number",
                "Entry Time",
                "Exit Time",
                "Parking Duration",
                "Parking Fee",
                "Rate",
            ]
            rows = [
                [
                    record.user.username,
                    record.user.license_number,
                    record.entry_time,
                    record.exit_time,
                    record.parking_duration,
                    record.parking_fee,
                    record.rate.rate_name if record.rate else "N/A",
                ]
                for record in queryset
            ]

        elif report_type == "payment":
            queryset = Payment.objects.all()
            if start_date:
                queryset = queryset.filter(payment_time__gte=start_date)
            if end_date:
                queryset = queryset.filter(payment_time__lte=end_date)

            header = ["Parking Record", "Amount", "Payment Time", "Is Successful"]
            rows = [
                [
                    payment.parking_record,
                    payment.amount,
                    payment.payment_time,
                    payment.is_successful,
                ]
                for payment in queryset
            ]

        elif report_type == "user":
            queryset = User.objects.all()
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)

            header = [
                "Username",
                "Email",
                "First Name",
                "Last Name",
                "Phone Number",
                "License Number",
                "Created At",
            ]
            rows = [
                [
                    user.username,
                    user.email,
                    user.first_name,
                    user.last_name,
                    user.phone_number,
                    user.license_number,
                    user.created_at,
                ]
                for user in queryset
            ]

        # Создание CSV файла
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)

        # Создание записи отчета
        report = Report.objects.create(report_type=report_type)
        report.file_path.save(
            f'{report_type}_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv',
            ContentFile(csv_file.getvalue()),
        )
        report.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"{report_type.capitalize()} report generated successfully!"
            )
        )
