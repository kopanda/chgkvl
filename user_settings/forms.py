from django import forms
from dal import autocomplete
from .models import UserSettings


class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = UserSettings
        fields = '__all__'
        widgets = {
            'person': autocomplete.ModelSelect2Multiple(url='person-autocomplete'),
            'teams': autocomplete.ModelSelect2Multiple(url='team-autocomplete'),
        }
