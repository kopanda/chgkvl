from django.contrib import admin
from .models import UserSettings
from .forms import UserSettingsForm


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    form = UserSettingsForm

