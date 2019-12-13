from django import forms
from dal import autocomplete
from django.forms.widgets import HiddenInput, RadioSelect
from .models import Attendance, Claim


class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = '__all__'
        widgets = {
            'team': autocomplete.ModelSelect2(url='/api/team'),
            'played': HiddenInput,
        }


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'person': autocomplete.ModelSelect2Multiple(url='/api/person'),
            'flag': RadioSelect,
            'team': HiddenInput,
        }
