from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import Event


@receiver(post_save, sender=Event)
def event_update(instance, **kwargs):
    if instance.tournament is not None and instance.name != instance.tournament.name:
        instance.update_from_rating()
        instance.save()
