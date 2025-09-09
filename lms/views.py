from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .paginators import StandardResultsSetPagination
from users.permissions import IsOwnerOrModer, IsOwnerOrAdmin
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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


# ---------- Stripe интеграция ----------

class StripeCreateProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description", "")
        if not title:
            return Response({"error": "title is required"}, status=status.HTTP_400_BAD_REQUEST)
        product = stripe.Product.create(name=title, description=description)
        return Response({"id": product.id, "name": product.name})


class StripeCreatePriceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        amount = request.data.get("amount")
        currency = request.data.get("currency", "usd")
        if not product_id or not amount:
            return Response({"error": "product_id and amount are required"}, status=status.HTTP_400_BAD_REQUEST)
        price = stripe.Price.create(
            unit_amount=int(amount),
            currency=currency,
            product=product_id,
        )
        return Response({"id": price.id, "unit_amount": price.unit_amount})


class StripeCheckoutSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        price_id = request.data.get("price_id")
        success_url = request.data.get("success_url", "http://localhost:8000/success")
        cancel_url = request.data.get("cancel_url", "http://localhost:8000/cancel")
        if not price_id:
            return Response({"error": "price_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return Response({"checkout_url": session.url})
