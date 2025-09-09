from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import youtube_only_validator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(
        validators=[youtube_only_validator], required=False
    )

    class Meta:
        model = Lesson
        fields = ["id", "title", "owner", "course", "video_link"]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "lessons",
            "lesson_count",
            "owner",
            "is_subscribed",
        ]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "user", "course"]
        read_only_fields = ["user"]
