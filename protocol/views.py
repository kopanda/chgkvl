from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
import requests
from .forms import ClaimForm, AttendanceForm
from .models import Claim
from rating.models import Person, Team, Tournament


# удалить
def new_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.save()
            return redirect('event_view')
    else:
        form = ClaimForm()
    return render(request, 'protocol/claim.html', {'form': form})


class AttendanceView(FormMixin, TemplateView):
    template_name = 'protocol/attendance.html'
    form_class = AttendanceForm

    def get_context_data(self, **kwargs):
        context = super(AttendanceView, self).get_context_data(**kwargs)
        x = Claim.objects.get(
            event__tournament__idtournament=kwargs['id'],
            team__idteam=kwargs['id']
        )
        players = Person.objects.none()

        if x.team:
            json = requests.get("https://rating.chgk.info/api/teams/%s/recaps.json/last/" % kwargs['id']).json()
            if len(json['players']) > 0:
                for idplayer in json['players']:
                    p, created = Person.objects.update_or_create(idplayer=idplayer)
                    if created or not p.json:
                        p.update()
                    players |= Person.objects.filter(idplayer=p.idplayer)

        context['team'] = Team.objects.get(idteam=kwargs['id'])
        context['tournament'] = Tournament.objects.get(idtournament=kwargs['id'])
        context['players'] = players

        return context
