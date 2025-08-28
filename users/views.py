from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from users.permissions import IsModer, IsOwner
from .models import CustomUser, Payment
from .serializers import (
    CustomUserSerializer, PaymentSerializer,
    UserProfileSerializer, UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action == "destroy":
            return [IsAdminUser()]
        elif self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwner() | IsModer()]
        return [IsAuthenticated()]


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated(), IsOwner() | IsModer()]
        return [IsAuthenticated()]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["date"]
    ordering = ["-date"]


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
