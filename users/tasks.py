from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, не заходивших в систему более 30 дней.
    """
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(is_active=True, last_login__lt=threshold)
    count = inactive_users.update(is_active=False)
    return f"Blocked {count} inactive users"
