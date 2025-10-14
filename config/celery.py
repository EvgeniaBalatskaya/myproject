import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Периодические задачи
app.conf.beat_schedule = {
    "check_inactive_users_daily": {
        "task": "users.tasks.block_inactive_users",
        "schedule": crontab(hour=0, minute=0),  # каждый день в полночь
    },
}

app.conf.timezone = settings.TIME_ZONE
