from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Lesson, Subscription

@shared_task
def send_lesson_update_email(lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
    except Lesson.DoesNotExist:
        return

    # Проверка: курс не обновлялся более 4 часов
    if lesson.updated_at and timezone.now() - lesson.updated_at < timedelta(hours=4):
        return

    subscriptions = Subscription.objects.filter(course=lesson.course)
    for sub in subscriptions:
        send_mail(
            subject=f"Новый урок в курсе {lesson.course.title}",
            message=f"Урок '{lesson.title}' обновлен. Посмотреть: http://example.com/courses/{lesson.course.id}/",
            from_email="no-reply@example.com",
            recipient_list=[sub.user.email],
        )
