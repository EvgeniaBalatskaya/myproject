from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonViewSet,
    SubscriptionViewSet,
    StripeCreateProductAPIView,
    StripeCreatePriceAPIView,
    StripeCheckoutSessionAPIView
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)
router.register(r"subscriptions", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path("", include(router.urls)),

    # Stripe endpoints
    path("stripe/product/", StripeCreateProductAPIView.as_view(), name="stripe-create-product"),
    path("stripe/price/", StripeCreatePriceAPIView.as_view(), name="stripe-create-price"),
    path("stripe/checkout/", StripeCheckoutSessionAPIView.as_view(), name="stripe-checkout"),
]
