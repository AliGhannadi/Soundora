from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Artist


@receiver(post_save, sender=Artist)
def update_user_is_artist(sender, instance, created, **kwargs):
    if created:
        instance.user.is_artist = True
        instance.user.save(update_fields=["is_artist"])
