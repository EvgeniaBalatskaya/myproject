from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Lesson, Subscription


@shared_task
def send_lesson_update_email(lesson_id):
    """
    Асинхронная рассылка писем подписчикам о новом или обновлённом уроке.
    Проверка — курс не должен обновляться чаще, чем раз в 4 часа.
    """
    try:
        lesson = Lesson.objects.select_related("course").get(id=lesson_id)
    except Lesson.DoesNotExist:
        return "Lesson not found"

    # Проверка — курс не обновлялся последние 4 часа
    if lesson.updated_at and timezone.now() - lesson.updated_at < timedelta(hours=4):
        return "Too early to send notifications"

    subscriptions = Subscription.objects.filter(course=lesson.course).select_related("user")

    sent_count = 0
    for sub in subscriptions:
        if not sub.user.email:
            continue
        send_mail(
            subject=f"📚 Обновление урока в курсе «{lesson.course.title}»",
            message=(
                f"Урок «{lesson.title}» был обновлён.\n"
                f"Посмотреть можно здесь: http://example.com/courses/{lesson.course.id}/"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=True,
        )
        sent_count += 1

    return f"Emails sent: {sent_count}"
