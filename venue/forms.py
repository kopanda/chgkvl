from django import forms
from .models import Event
from rating.models import Tournament
from datetime import datetime


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'datetime',
            'location',
            'tournament',
            'name',
            'description',
            'difficulty',
            'teams_main',
            'teams_disc',
            'teams_free',
            'fee_main',
            'fee_main_rub',
            'fee_disc',
            'fee_disc_rub',
            'fee_comment',
            'pay_before',
            'payment',
            'currency',
            'payment_rub',
            'payment_method',
            'payment_details',
            'payment_day',
            'notify_by',
            'fee_player',
            'fee_points',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        event_datetime = instance.datetime if instance else datetime.utcnow()
        t = Tournament.objects.none()
        for i in ['Строго синхронный', 'Синхрон', 'Асинхрон']:
            t = (t | Tournament.objects.filter(type_name=i))
        tournaments = t.filter(
            date_start__lte=event_datetime,
            date_end__gte=event_datetime,
        ).order_by('-type_name')
        self.fields['tournament'].queryset = tournaments
