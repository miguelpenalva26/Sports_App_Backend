from rest_framework import serializers
from .models import Facility, Booking


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source="facility.name", read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["user"]