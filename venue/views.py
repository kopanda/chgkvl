from django.shortcuts import render
from django.views.generic.base import TemplateView
from rating.models import Team
from .models import Event


class EventView(TemplateView):
    template_name = 'venue/event.html'

    def get_context_data(self, **kwargs):
        context = super(EventView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context


class EventTeamView(TemplateView):
    template_name = 'venue/event.html'

    def get_context_data(self, **kwargs):
        context = super(EventTeamView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        context['team'] = Team.objects.get(idteam=kwargs['id'])

        return context


class VueEventView(TemplateView):
    template_name = 'venue/vue-event.html'

    def get_context_data(self, **kwargs):
        context = super(VueEventView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context
