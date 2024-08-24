import csv
from django.http import HttpResponse
from django.utils import timezone

# from app_accounts.models import User
from app_car_moderation.models import ParkingRecord, Payment

from django.utils.html import strip_tags
import os
from django.template.loader import render_to_string

from django.core.mail import send_mail
from dotenv import load_dotenv

from app_parking.celery import app
from django.contrib.auth import get_user_model

User = get_user_model()


def export_users_to_csv(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="users_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "Username",
            "Email",
            "Full Name",
            "Phone Number",
            "Address",
            "Created At",
        ]
    )
    for user in queryset:
        writer.writerow(
            [
                user.username,
                user.email,
                user.full_name,
                user.phone_number,
                user.address,
                user.created_at,
            ]
        )
    return response


def export_parking_records_to_csv(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="parking_records_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "User",
            "license_number",
            "Entry Time",
            "Exit Time",
            "Parking Duration",
            "Parking Fee",
            "Rate",
            "Is Paid",
            "Is Parked",
        ]
    )
    for record in queryset:
        writer.writerow(
            [
                record.user.username,
                record.entry_time,
                record.exit_time,
                record.parking_duration,
                record.parking_fee,
                record.rate.rate_name,
                record.is_paid,
                record.is_parked,
            ]
        )
    return response


def export_payments_to_csv(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="payments_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    )
    writer = csv.writer(response)
    writer.writerow(["Parking Record", "Amount", "Payment Time", "Is Successful"])
    for payment in queryset:
        writer.writerow(
            [
                payment.parking_record,
                payment.amount,
                payment.payment_time,
                payment.is_successful,
            ]
        )
    return response


@app.task
def send_balance_warning_emails():
    users = User.objects.filter(money_balance__lt=15)
    print(users)

    for user in users:
        subject = "Warning: Low Balance"
        html_message = render_to_string(
            "app_report/balance_warning.html", {"user": user}
        )
        plain_message = strip_tags(html_message)
        from_email = os.getenv("EMAIL_HOST_USER")
        to_email = user.email

        send_mail(
            subject, plain_message, from_email, [to_email], html_message=html_message
        )
