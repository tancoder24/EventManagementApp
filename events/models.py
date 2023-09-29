from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from datetime import timedelta

from . import utils

class User(AbstractUser):
    def __str__(self):
        return self.username 

class Venue(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Venue Name")
    capacity = models.PositiveIntegerField(default=0, help_text="Venue Capacity")
    amenities = models.TextField(help_text="Amenities available at Venue")

    def __str__(self):
        return self.name
    
    def get_all_events(self):
        return self.event_set.filter(date__gte=timezone.now().date())

    def get_booked_dates(self):
        return Event.objects.filter(location=self).values_list('date', flat=True).distinct()

    def get_available_dates(self):
        event_dates = set(self.get_booked_dates())
        
        # if no booked dates return empty array else max() will bring error
        if not event_dates: return ["No bookings"]
        
        available_dates = []
        current_date = timezone.now().date()
        while current_date <= max(event_dates):
            if current_date not in event_dates:
                available_dates.append(current_date)
            current_date += timedelta(days=1)

        return available_dates


def validate_future_date(value):
    if value < timezone.now().date() + timezone.timedelta(days=1):
        raise ValidationError("Event date must be in the future.")
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(validators=[validate_future_date])
    time = models.TimeField()
    location = models.ForeignKey(Venue, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    category = models.CharField(max_length=255, choices=utils.CATEGORY_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

    class Meta:
        unique_together = ('user', 'event')
