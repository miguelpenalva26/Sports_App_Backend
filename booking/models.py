from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Facility(models.Model):
    name = models.CharField(max_length=100)
    is_indoor = models.BooleanField(default=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Booking(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        # Prevent end time before start time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

        # Check overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            facility=self.facility,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )

        # Exclude current instance when updating
        if self.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("This time slot is already booked.")

    def __str__(self):
        return f"{self.facility.name} - {self.date} ({self.start_time}-{self.end_time})"