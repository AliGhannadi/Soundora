from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import caches
from .models import Music


@receiver([post_save, post_delete], sender=Music)
def delete_music_list_cache(sender, instance, **kwargs):
    caches["page_cache"].clear()
    