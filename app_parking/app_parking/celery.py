import os

from celery.schedules import crontab
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_parking.settings")


app = Celery("app_parking")


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "task1": {
        "task": "app_report.utils.send_balance_warning_emails",
        # "schedule": crontab(minute="*", hour="1-23"),
        # "schedule": crontab(day_of_week=1, hour=0),
        "schedule": crontab(minute="*"),
        # "schedule": crontab(day_of_week="*", hour=0),
    }
}
app.conf.timezone = "UTC"
