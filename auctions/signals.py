from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Watchlist


@receiver(post_save, sender=User)
def create_watchlist(sender, instance, created, **kwargs):
    if created:
        Watchlist.objects.create(user=instance)

