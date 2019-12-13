from django.shortcuts import render
from dal import autocomplete
from user_settings.models import UserSettings
from .models import Team, Person


class TeamAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Team.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        else:
            if self.request.user.is_authenticated:
                return UserSettings.objects.get(user=self.request.user).teams.all()

        return qs


class PersonAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # town = 'Владивосток'

        if self.q:
            qs = Person.objects.filter(fio__istartswith=self.q)
        else:
            qs = Person.objects.all()

        return qs
