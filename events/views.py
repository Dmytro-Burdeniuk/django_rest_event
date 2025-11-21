from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import viewsets, generics, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied

from .models import Event, EventRegistration
from .serializers import (
    UserRegisterSerializer,
    EventSerializer,
    EventRegistrationSerializer,
    LoginSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        raw_password = serializer.validated_data.get("password")
        if raw_password:
            user.set_password(raw_password)
            user.save()
        Token.objects.create(user=user)


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search events by title (case insensitive)",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Event.objects.all()
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        event = self.get_object()
        if event.created_by != self.request.user:
            raise PermissionDenied("You did not create this event")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user:
            raise PermissionDenied("You did not create this event")
        instance.delete()


class EventRegistrationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        registration = serializer.save(user=self.request.user)
        user = registration.user
        event = registration.event

        if user.email:
            message = (
                f"Hi {user.username},\n\n"
                f"You registered for '{event.title}' "
                f"on {event.date} at {event.location}.\n\n"
                "Thank you!"
            )

            send_mail(
                subject="Event registration",
                message=message,
                from_email=None,
                recipient_list=["dmytroburdenuk@gmail.com"], # my personal email for testing email sending
                fail_silently=False,
            )
