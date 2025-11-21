from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events'
    )

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'
