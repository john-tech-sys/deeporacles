from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from circles.models import Forum
from contrib.models import *
from home.models import Post


@receiver(post_save, sender=Comment)
def afterComment(sender, instance, created, **kwargs):
	if not instance.author == instance.post.author:
		post = instance.post
		if post.comments.count() == 1:
			for receiver in post.post_notify_people.all():
				text_preview = "{0} commented on your post {1}".format(instance.user.profile.user(), post.content)
				Notification.objects.create(sender=instance.user, text_preview=text_preview, receiver=receiver, notifications_type=7, notifications_obj=2, post=post, comments=instance)
		else:
			for receiver in post.post_notify_people.all():
				text_preview = "{0} and {1} others commented on your post {2}".format(instance.user.profile.user(), post.comments.count() , post.content)
				Notification.objects.create(sender=instance.user, text_preview=text_preview, receiver=receiver, notifications_type=7, notifications_obj=2, post=post, comments=instance)
@receiver(post_save, sender=Post)
def afterPost(sender, instance, **kwargs):
	instance.post_notify_people.add(instance.user)


@receiver(post_save, sender=Notification)
def AfterNotifies(sender, instance, **kwargs):
    notify_group_name = 'notify_%d'% instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name,
        {'type': 'chat_message', 'notify': render_to_string('notification/notify.html', {'notify': instance, 'request.user': instance.receiver})})


@receiver(post_delete, sender=Notification)
def AfterNotifiesDelete(sender, instance, **kwargs):
    notify_group_name = 'notify_%d'% instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name,
        {'type': 'chat_message', 'notify_delete': instance.pk})


@receiver(post_save, sender=Forum)
def AfterGroup(sender, instance, **kwargs):
    instance.group_members.add(instance.group_admin)
    instance.group_admin.groups.add(instance)