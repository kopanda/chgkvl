from rest_framework import viewsets, filters
from .models import UserSettings
from .serializers import UserSettingsSerializer


class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    filter_backends = (filters.SearchFilter,)
