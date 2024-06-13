
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save, pre_save, post_init
from django.dispatch import receiver
from .models import Profile



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()