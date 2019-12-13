from django.apps import AppConfig
from django.db.models.signals import post_save


class VenueConfig(AppConfig):
    name = 'venue'
    verbose_name = 'Мероприятия'

    def ready(self):
        from .models import Event
        from .signals import event_update
        post_save.connect(event_update, sender=Event)
