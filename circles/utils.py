
from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Forum

@receiver(post_save, sender=Forum)
def AfterGroup(sender, instance, **kwargs):
    instance.forum_members.add(instance.forum_admin)
    instance.forum_admin.profile.forums.add(instance)