from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventRegistrationViewSet, RegisterView, LoginView

router = DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("registrations", EventRegistrationViewSet, basename="registration")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
