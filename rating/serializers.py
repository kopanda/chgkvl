from rest_framework import serializers
from .models import Person, Team, Tournament


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'surname', 'name', 'patronymic', '__str__']
        read_only_fields = ['__str__']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'town', '__str__']
        read_only_fields = ['__str__']


class TournamentSerializer(serializers.ModelSerializer):
    organizers = PersonSerializer(many=True)
    authors = PersonSerializer(many=True)
    game_jury = PersonSerializer(many=True)
    jury_of_appeal = PersonSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'questions_total', 'type_name', 'tournament_in_rating', 'site_url',
                  'orgcommittee', 'authors', 'game_jury', 'jury_of_appeal']
