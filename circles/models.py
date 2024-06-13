
# Create your models here.
from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth import get_user_model
from froala_editor.fields import FroalaField
from django.db.models import *
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

# from chat.utils import find_or_create_private_chat
from contrib.models import Notification, Report


# def get_forum_img_path(self, filename):
#     	return 'forum/' + str(self.pk) + filename
def get_forum_img_path(instance, filename):
	return 'forums/{0}/{1}'.format(instance.forum_name, filename)
def get_space_img_path(instance, filename):
	return 'spaces/{0}/{1}'.format(instance.space_name, filename)


class Forum(models.Model):
    forum_admin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='forum_author', null=True, blank=True)
    forum_sub_admin = models.ManyToManyField(get_user_model(), related_name='forum_sub_author', blank=True)
    forum_cover_photo = models.ImageField(default='default/014.jpeg', upload_to=get_forum_img_path, null=True, blank=True)
    forum_name = models.CharField(max_length=100, default="Forum")
    picture = models.ImageField(default='default/default-avatar.png', upload_to=get_forum_img_path, blank=True, null=True)
    slug = AutoSlugField(populate_from='forum_name', unique=True)
    forum_bio = FroalaField('Forum Details', blank=True, null=True)
    date_created = models.DateTimeField(('date created'), auto_now_add = True, blank=True, null=True)
    forum_members = models.ManyToManyField(get_user_model(), related_name='forum_members', blank=True)
    forum_members_waiting = models.ManyToManyField(get_user_model(), related_name='forum_waiting_members', blank=True)
    invite_forum_members = models.ManyToManyField(get_user_model(), related_name='invited_forum_members', blank=True)
    forum_members_blocked = models.ManyToManyField(get_user_model(), related_name='forum_blocked_members', blank=True)
    followers = models.ManyToManyField(get_user_model(), blank=True, related_name= 'forum_followers')
    private_mode = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(get_user_model(), related_name='forum_who_hid', on_delete=models.CASCADE, null=True, blank=True)
    date_hidden = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    reports = GenericRelation(Report)
    notifications		= GenericRelation(Notification)

    def __str__(self):
        return str(self.forum_name)

    def connect_user(self, user):
        """
        return true if user is added to the users list
        """
        is_user_added = False
        if not user in self.forum_members.all():
            self.forum_members.add(user)
            self.save()
            is_user_added = True
        elif user in self.forum_members.all():
            is_user_added = True
        return is_user_added


    def disconnect_user(self, user):
        """
        return true if user is removed from the users list
        """
        is_user_removed = False
        if user in self.forum_members.all():
            self.forum_members.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed 

    def total_posts(self):
        from home.models import Post  # import Post model here to avoid circular import
        return Post.objects.filter(forum__id=self.id, active=True, hidden=False, is_question=False).count()
    def total_questions(self):
        from home.models import Post  # import Post model here to avoid circular import
        return Post.objects.filter(forum__id=self.id, active=True, hidden=False, is_question=True).count()

    def get_forum_api_follow_url(self):
        return reverse('forum_api_follow', kwargs={'pk': self.pk})

    def get_forum_api_join_url(self):
        return reverse('forum_api_join', kwargs={'pk': self.pk})


    @property
    def forum_nm(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "Forum-%s" % self.id


class Circles(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="circles")
    connections = models.ManyToManyField(get_user_model(), blank=True, related_name="connections")
    followers = models.ManyToManyField(get_user_model(), blank=True, related_name= 'user_followers')
    following = models.ManyToManyField(get_user_model(), blank=True, related_name='user_following')
    forums = models.ManyToManyField("Forum", blank=True, related_name='user_forums')
    # set up the reverse relation to GenericForeignKey
    notifications = GenericRelation(Notification)

    # def __str__(self):
    #     return self.user
    
    class Meta:
        verbose_name = 'Circle'
        verbose_name_plural = 'Circles'

    @property
    def get_cname(self):
        """
        For determining what kind of object is associated with a Notification
        """
        return "Circles"

    def is_mutual_friend(self, connection):
        """
        Is this a connection?
        """
        if connection in self.connections.all():
            return True
        return False

    def get_api_follow_url(self):
        return reverse('profile_api_follow', kwargs={'pk': self.pk})
