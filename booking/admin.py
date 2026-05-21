from django.contrib import admin
from .models import Facility, Booking


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "is_indoor")
    search_fields = ("name", "location")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("facility", "user", "date", "start_time", "end_time")
    list_filter = ("facility", "date")
    search_fields = ("facility__name", "user__username")