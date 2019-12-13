from rest_framework import serializers
from .models import Attendance, Claim
from rating.serializers import TeamSerializer


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'datetime', 'team', 'name', 'event', 'played']


class ClaimExpandedSerializer(serializers.ModelSerializer):
    team = TeamSerializer(many=False)
    class Meta:
        model = Claim
        fields = ['id', 'datetime', 'team', 'name', 'played']
