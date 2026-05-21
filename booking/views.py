from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import requests

from .models import Facility, Booking
from .serializers import FacilitySerializer, BookingSerializer

API_KEY = "5c02c7e9f9af17f28de35219b90fbbc5"

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [permissions.IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Booking.objects.filter(user=self.request.user)

        facility = self.request.query_params.get('facility')
        date = self.request.query_params.get('date')

        if facility:
            queryset = queryset.filter(facility_id=facility)

        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def perform_create(self, serializer):
        facility = serializer.validated_data['facility']
        date = serializer.validated_data['date']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        if end_time <= start_time:
            raise ValidationError("End time must be after start time")

        existing_bookings = Booking.objects.filter(
            facility=facility,
            date=date
        )

        for booking in existing_bookings:
            if start_time < booking.end_time and end_time > booking.start_time:
                raise ValidationError("This time slot is already booked")

        serializer.save(user=self.request.user)    

@api_view(['GET'])
def recommendation(request):
    date = request.GET.get('date')
    hour = request.GET.get('hour')

    if not date or not hour:
        return Response({"error": "Missing data"}, status=400)

    url = f"https://api.openweathermap.org/data/2.5/forecast?q=York,GB&appid={API_KEY}"
    res = requests.get(url)
    data = res.json()

    target_hour = int(hour)

    closest = None
    min_diff = 999

    for item in data["list"]:
        dt_txt = item["dt_txt"]

        if dt_txt.startswith(date):
            forecast_hour = int(dt_txt.split(" ")[1].split(":")[0])
            diff = abs(forecast_hour - target_hour)

            if diff < min_diff:
                min_diff = diff
                closest = item

    if not closest:
        return Response({"advice": "No weather data"})

    weather = closest["weather"][0]["main"]

    if weather in ["Rain", "Drizzle", "Thunderstorm"]:
        indoor = Facility.objects.filter(is_indoor=True).first()
        return Response({
            "advice": "Rain expected → use indoor",
            "recommended_facility": indoor.name if indoor else None
        })
    else:
        outdoor = Facility.objects.filter(is_indoor=False).first()
        return Response({
            "advice": "Good weather → outdoor is fine",
            "recommended_facility": outdoor.name if outdoor else None
        })