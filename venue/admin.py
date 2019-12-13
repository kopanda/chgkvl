from django.contrib import admin
from .models import Location, Event
from .forms import EventForm


admin.site.register(Location)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm

