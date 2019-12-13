from abc import ABC

from rest_framework import serializers
from .models import Location, Event
from rating.serializers import TournamentSerializer
from protocol.serializers import ClaimExpandedSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class RoundingDecimalField(serializers.DecimalField):
    def validate_precision(self, value):
        return value


class EventSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer(many=False)
    location = LocationSerializer(many=False)
    claims = ClaimExpandedSerializer(many=True)
    fee_main_rub = RoundingDecimalField(max_digits=8, decimal_places=0)
    fee_disc_rub = RoundingDecimalField(max_digits=8, decimal_places=0)
    fee_player = RoundingDecimalField(max_digits=8, decimal_places=0)
    fee_points = RoundingDecimalField(max_digits=8, decimal_places=0)

    class Meta:
        model = Event
        fields = ['id', 'datetime', 'location', 'tournament', 'name', 'description', 'difficulty',
                  'fee_main_rub', 'fee_disc_rub', 'fee_comment', 'fee_player', 'fee_points',
                  'claims']
