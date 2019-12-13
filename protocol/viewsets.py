from rest_framework import viewsets, filters
from .models import Attendance, Claim
from .serializers import AttendanceSerializer, ClaimSerializer, ClaimExpandedSerializer
from rest_framework.permissions import AllowAny


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.SearchFilter,)


class ClaimViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    filter_backends = (filters.SearchFilter,)


class ClaimExpandedViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Claim.objects.all()
    serializer_class = ClaimExpandedSerializer
    filter_backends = (filters.SearchFilter,)
