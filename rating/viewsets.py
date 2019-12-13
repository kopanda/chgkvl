from rest_framework import viewsets, filters, pagination
from .models import Person, Team, Tournament
from .serializers import PersonSerializer, TeamSerializer, TournamentSerializer


class SearchPagination(pagination.PageNumberPagination):
    page_size = 5


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    pagination_class = SearchPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'surname', 'name', 'patronymic')


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = SearchPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'name', 'town')


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    filter_backends = (filters.SearchFilter,)

