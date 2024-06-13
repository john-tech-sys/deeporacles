
from deeporacles import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
import uuid as uuid
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from contrib.models import BaseModel, Like, Notification, Comment, PostLocation, Report, Tag
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from froala_editor.fields import FroalaField
from django.core.validators import FileExtensionValidator
from deeporacles.settings import VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, IMAGE_EXTENSIONS, MAX_IMAGE_SIZE, MAX_VIDEO_SIZE, \
    MAX_AUDIO_SIZE
from deeporacles.validators import FileSizeValidator
from circles.models import Forum
import re

def get_update_upload_path(instance, filename):
	return 'updates/{0}/{1}/{2}'.format(instance.update.user.email, instance.update.id ,filename)


def get_post_upload_path(instance, filename):
	return 'posts/{0}/{1}/{2}'.format(instance.post.author.email, instance.post.id ,filename)

def get_comment_file_path(instance, filename):
	return 'comments/{0}/{1}'.format(instance.post.author.email, instance.post.id ,filename)

def get_reply_file_path(instance, filename):
	return 'replies/{0}/{1}'.format(instance.post.author.email, instance.post.id ,filename)
# Create your models here.



class Space(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    details = FroalaField('Space Details', blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    enable = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("hub",  kwargs={"slug": self.slug})

    def total_posts(self):
        return Post.objects.filter(space__id=self.id).count()



class Copyright(BaseModel):
    """Model to store all copyright."""

    name = models.CharField(max_length=300)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SoundCategory(BaseModel):
    """Model to store all copyright."""

    name = models.CharField(max_length=300)
    icon = models.ImageField(upload_to='system/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Sound(BaseModel):
    """Model to store all sounds."""

    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sound_file = models.FileField(upload_to='uploads/sounds/')
    sound_cover = models.ImageField(upload_to='uploads/cover/', null=True, blank=True)
    copyright = models.ForeignKey(Copyright, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(SoundCategory, on_delete=models.CASCADE, null=True, blank=True)
    is_extracted_audio = models.BooleanField(default=False)

    def __str__(self):
        return self.name or 'Extracted Audio: {}'.format(
            self.profile.user.username
        )

class CustomFK(models.ForeignKey):
	def contribute_to_class(self, cls, name, private_only=False, **kwargs):
		super().contribute_to_class(cls, name, private_only=False, **kwargs)
		self.remote_field.related_name = "_".join(re.findall('[A-Z][^A-Z]*', cls.__name__))

class Snippet(models.Model):
    # uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author 			= CustomFK(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)s')
    post 			= CustomFK('Post', null=True, blank=True, on_delete=models.CASCADE, related_name='%(class)s')
    like = models.ManyToManyField(get_user_model(), blank=True, related_name='%(app_label)s_likes_%(class)s', related_query_name='%(app_label)s_likes_%(class)s')
    love = models.ManyToManyField(get_user_model(), blank=True, related_name='%(app_label)s_love_%(class)s', related_query_name='%(app_label)s_love_%(class)s')
    sad = models.ManyToManyField(get_user_model(), blank=True, related_name='%(app_label)s_sad_%(class)s', related_query_name='%(app_label)s_sad_%(class)s')
    wow = models.ManyToManyField(get_user_model(), blank=True, related_query_name='%(app_label)s_wow_%(class)s', related_name='%(app_label)s_wow_%(class)s')
    haha = models.ManyToManyField(get_user_model(),  blank=True, related_name='%(app_label)s_haha_%(class)s', related_query_name='%(app_label)s_haha_%(class)s')
    angry = models.ManyToManyField(get_user_model(),  blank=True,related_query_name='%(app_label)s_angry_%(class)s', related_name='%(app_label)s_angry_%(class)s')
    shared = models.ManyToManyField(get_user_model(), blank=True, related_name='%(app_label)s_shared_%(class)s', related_query_name='%(app_label)s_shared_%(class)s')
    DatePublished = models.DateTimeField(default=timezone.now)

    def reacts_count(self):
        reacts = int(self.like.count()) + int(self.love.count())+ int(self.sad.count())+ int(self.wow.count())+ int(self.haha.count())+ int(self.angry.count())

        if reacts == 1:
            return str("1 Reaction")
        elif reacts == 0:
            return str(reacts) + " Reactions" 
        else:
            return str(reacts) + " Reactions" 
        
    def react_count(self):
        reacts = int(self.like.count()) + int(self.love.count())+ int(self.sad.count())+ int(self.wow.count())+ int(self.haha.count())+ int(self.angry.count())

        return str(reacts)

    def like_count(self):
        reacts = int(self.like.count())
        return str(reacts)

    # def like_count(self):
    #     reacts = int(self.like.count())
    #     return str(reacts) + " Like" 

    def love_count(self):
        reacts = int(self.love.count())
        return str(reacts)

    def sad_count(self):
        reacts = int(self.sad.count())
        return str(reacts)

    def wow_count(self):
        reacts = int(self.wow.count())
        return str(reacts)

    def laugh_count(self):
        reacts = int(self.haha.count())
        return str(reacts)

    def angry_count(self):
        reacts = int(self.angry.count())
        return str(reacts)

    class Meta:
        abstract = True
        ordering = ['-DatePublished']


class Post(Snippet):
    content = FroalaField('Content', blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    space = models.ForeignKey(Space, null=True, blank=True, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, null=True, blank=True, on_delete=models.CASCADE , related_name='post_forum')
    picture = models.ImageField( upload_to='posts/image_post_file', default=None, blank=True, null=True)
    title = models.CharField('Title', max_length=100, blank=True,  null=True)
    Audio_file = models.FileField('audio', upload_to='posts/audio_post_file', blank=True, null=True,
                                    validators=[FileExtensionValidator(allowed_extensions=AUDIO_EXTENSIONS)])
    Video_file = models.FileField('video', upload_to='posts/video_post_file', blank=True, null=True,
                                    validators=[FileExtensionValidator(allowed_extensions=VIDEO_EXTENSIONS)])
    slug = AutoSlugField(populate_from='title', unique=True)
    edited = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    post_notify_people = models.ManyToManyField(get_user_model(), blank=True, related_name='post_notified_users')
    hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(get_user_model(), related_name='post_who_hid', on_delete=models.CASCADE, null=True, blank=True)
    date_hidden = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE, null=True, blank=True)
    video_gif = models.FileField(upload_to='post/gifs/', null=True, blank=True)
    is_pornographic = models.BooleanField(default=False)
    is_downloadable = models.BooleanField(default=False)
    is_question = models.BooleanField(default=False)
    share_pointer = models.ForeignKey('self', on_delete=models.CASCADE, related_name='shared_post', null=True, blank=True)
    uploaded_location = models.ForeignKey(PostLocation, on_delete=models.CASCADE, null=True, blank=True)
    reports = GenericRelation(Report)
    comments = GenericRelation(Comment)
    notifications = GenericRelation(Notification)
    tags = GenericRelation(Tag)
    likes = GenericRelation(Like)

    # def __str__(self):
    #     return self.title()

    class Meta:
        indexes = [
            models.Index(fields=['edited', 'id']),
            models.Index(fields=['-edited', '-id'])]
        ordering = ('-edited',)

    # def __str__(self):
    #     return self.title
        
    # def __unicode__(self):
    #     return self.title

    def get_title(self, *arg, **kwargs):
        if self.title:
            return self.title
        else:
            titl = ''
            return titl

    def get_picture(self):
        return self.picture

    # def get_absolute_url(self):
    #     return reverse('post_detail', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('details', kwargs={'slug': self.slug})

    def get_like_url(self):
        return reverse('like-post', kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse('post_api_like', kwargs={'pk': self.pk})

    def get_api_report_url(self):
        return reverse('post_api_report', kwargs={'pk': self.pk})

    def get_api_save_url(self):
        return reverse('post_api_save', kwargs={'pk': self.pk})

    @property
    def num_comments(self):
        return self.comments.all().count()

    @property
    def last_comment(self):
        return self.comments.all().latest("comment_date")

    @property
    def get_content_type(self):
        instance = self 
        content_type = ContentType.object.get_for_model(instance.__class__)
        return content_type

    # def save(self, *arg, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.user_name)
    #     super(Post, self).save(*arg, **kwargs)




class PostView(BaseModel):
    """Record all views in posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        
        if self.post.title:
            return '{} has viewed {}'.format(
                self.user.profile.name,
                self.post.title[:20]    
            )
        else: 
            return '{} has viewed {}'.format(
                self.user.profile.name,
                self.post.content[:20]    
            )
    class Meta:
        unique_together = ('user', 'post',)


class Share(models.Model):
    user        = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    posts    = models.ManyToManyField(Post, blank=True)
    date_posted   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return "Share id: %s" %(self.id)


class PostFiles(Snippet):
	media = models.FileField(upload_to=get_post_upload_path, blank=True, null=True)


class Savedpost(models.Model):
	posts = models.ManyToManyField(Post, related_name='s_post' )
	user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='sp_user', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def users_all_saved_posts(self):
		all_saved_posts = Savedpost.objects.filter(user = self.user).order_by('-created_at')
		lst = []
		for item in all_saved_posts:
			lst.append(item.post.id)
		print(lst)
		return lst


class Update(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    active = models.BooleanField(default=True)
    content = models.TextField(blank=True, null=True)
    media = models.FileField(upload_to=get_update_upload_path, blank=True, null=True)
    video_gif = models.FileField(upload_to='updates/gifs/', null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    comments = GenericRelation(Comment)
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE, null=True, blank=True)
    tag_users = models.ManyToManyField(get_user_model(), blank=True, related_name='tag_users')
    hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(get_user_model(), related_name='update_who_hid', on_delete=models.CASCADE, null=True, blank=True)
    date_hidden = models.DateTimeField(null=True, blank=True)
    is_pornographic = models.BooleanField(default=False)
    reports = GenericRelation(Report)
    notifications = GenericRelation(Notification)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.slug()

    @property
    def num_comments(self):
        return self.comments.all().count()

    @property
    def last_comment(self):
        return self.comments.all().latest("comment_date")

