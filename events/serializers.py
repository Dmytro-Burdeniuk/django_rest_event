from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventRegistration


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "organizer",
            "created_by",
        ]


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    event_title = serializers.ReadOnlyField(source="event.title")

    class Meta:
        model = EventRegistration
        fields = ["id", "event", "event_title", "user", "created_at"]
