import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Пример periodic tasks через beat (можно потом перенести в tasks.py)
from celery.schedules import crontab

app.conf.beat_schedule = {
    "check_inactive_users": {
        "task": "users.tasks.block_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # каждый день в 00:00
    },
}
app.conf.timezone = settings.TIME_ZONE
