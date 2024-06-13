from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

object_viewed_signal = Signal()


user_logged_in = Signal()

