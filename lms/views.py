from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwnerOrModer, IsOwnerOrAdmin

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action == "destroy":
            # удалять может только владелец или админ
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated(), IsOwnerOrModer()]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "retrieve", "list", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrModer()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
