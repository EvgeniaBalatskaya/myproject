from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course, Lesson
from django.urls import reverse

User = get_user_model()

class CourseLessonPermissionsTest(APITestCase):
    def setUp(self):
        # Создаем обычного пользователя
        self.user = User.objects.create_user(email="user@example.com", password="password")
        # Создаем модератора
        self.moder = User.objects.create_user(email="moder@example.com", password="password")
        self.moder.groups.create(name="Moderators")
        # Создаем другой объект для проверки чужого доступа
        self.other_user = User.objects.create_user(email="other@example.com", password="password")

        # Курсы и уроки
        self.course = Course.objects.create(title="Course 1", description="Desc", owner=self.user)
        self.lesson = Lesson.objects.create(title="Lesson 1", course=self.course, owner=self.user)

    def test_owner_can_edit_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.patch(url, {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, "Updated")

    def test_other_user_cannot_edit_course(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.patch(url, {"title": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moder_can_edit_any_course(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.patch(url, {"title": "ModerEdit"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moder_cannot_delete_course(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("course-detail", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lesson-detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)