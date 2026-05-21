from rest_framework.routers import DefaultRouter
from .views import FacilityViewSet, BookingViewSet
from .views import recommendation
from django.urls import path

router = DefaultRouter()
router.register(r'facilities', FacilityViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls 

urlpatterns += [
    path('recommendation/', recommendation),
]