from rest_framework import viewsets, filters
from .models import Location, Event
from .serializers import LocationSerializer, EventSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = (filters.SearchFilter,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.SearchFilter,)