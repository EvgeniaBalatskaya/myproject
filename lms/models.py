from django.db import models
from users.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    video_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # для уведомлений через Celery

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.email} → {self.course.title}"
