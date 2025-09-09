from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course, Lesson, Subscription

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
        self.lesson = Lesson.objects.create(
            title="Lesson 1", course=self.course, owner=self.user, video_link="https://youtube.com/test"
        )

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

    def test_lesson_with_wrong_link_rejected(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lesson-list")
        data = {
            "title": "Bad link",
            "course": self.course.id,
            "owner": self.user.id,
            "video_link": "https://example.com/video",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="password")
        self.course = Course.objects.create(title="Course 1", description="Desc", owner=self.user)

    def test_user_can_subscribe_and_unsubscribe(self):
        self.client.force_authenticate(user=self.user)

        # подписка
        url = reverse("subscription-list")
        response = self.client.post(url, {"course": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # отписка
        sub = Subscription.objects.get(user=self.user, course=self.course)
        url = reverse("subscription-detail", args=[sub.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
