from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .paginators import StandardResultsSetPagination
from users.permissions import IsOwnerOrModer, IsOwnerOrAdmin


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated(), IsOwnerOrModer()]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "retrieve", "list", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrModer()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
