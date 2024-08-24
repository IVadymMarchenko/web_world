
from django.core.management.base import BaseCommand
from app_report.utils import send_balance_warning_emails


class Command(BaseCommand):
    help = "Send balance warning emails to users with low balance"

    def handle(self, *args, **kwargs):
        send_balance_warning_emails()
        self.stdout.write(
            self.style.SUCCESS("Successfully sent balance warning emails")
        )
