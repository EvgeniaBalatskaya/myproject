from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

@shared_task
def block_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(last_login__lt=threshold, is_active=True)
    inactive_users.update(is_active=False)
