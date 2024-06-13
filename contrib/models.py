from autoslug import AutoSlugField
from django.utils import timezone
from django.db import models
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from deeporacles import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.fields import GenericRelation
from utils.new_utils import unique_key_generator, unique_slug_generator
from django.contrib.contenttypes.models import ContentType
from utils.signals import user_logged_in, object_viewed_signal
from utils.utils import get_client_ip
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid as uuid
from django.db import models


FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION= getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


class BaseModel(models.Model):
    """Base model for Tikup infrastructure."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At', db_index=True)
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Last Modified At')

    class Meta:
        """Define meta params for model."""

        abstract = True
        ordering = ('-created_at',)



def get_comment_upload_path(instance, filename):
	return 'comments/{0}/{1}/{2}'.format(instance.user.email, instance.id ,filename)


class PostLocation(BaseModel):
    """Store location of posts."""

    ip_address = models.GenericIPAddressField()
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.ip_address

class Report(models.Model):
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reported_by', null=True, blank=True)
    verb = models.CharField(max_length=255, unique=False, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='rp_content_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.reported_by


# notification
class Notification(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="notif_from_user",  blank=True, null=True )
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="notif_to_user",  blank=True, null=True )
    text_preview = models.CharField(max_length=255, blank=True)
    is_seen = models.BooleanField(default=False)
    when = models.DateTimeField(auto_now_add=True)
    redirect_url = models.URLField(max_length=500, null=True, unique=False, blank=True, help_text="The URL to be visited when a notification is clicked.")
    # See article: https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='n_content_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-when']


    def __str__(self):
        return self.text_preview

    def get_content_object_type(self):
        return str(self.content_object.get_cname)


class SearchTerm(models.Model):
    hit = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=now)
    q = models.CharField(max_length=500, null=True, blank=True) 
    search_date = models.DateTimeField(auto_now_add=True) 
    ip_address = models.GenericIPAddressField() 
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    tracking_id = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return self.q


class Search(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True, related_name='search_user')
    searched = models.CharField(max_length=100, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date  = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username() + " searched for " + self.searched + " on " + str(self.date)



class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self, model_class, model_queryset=False):
        c_type = ContentType.objects.get_for_model(model_class)
        qs = self.filter(content_type=c_type)
        if model_queryset:
            viewed_ids = [x.object_id for x in qs]
            return model_class.objects.filter(pk__in=viewed_ids)
        return qs


class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self._db)

    def by_model(self, model_class, model_queryset=False):
        return self.get_queryset().by_model(model_class, model_queryset=model_queryset)


class ObjectViewed(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='obs_user')
    ip_address = models.CharField(max_length=220, blank=True, null=True) #IP Field
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return "%s viewed on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) # instance.__class__
    user = None
    if request.user.is_authenticated():
        user = request.user
    new_view_obj = ObjectViewed.objects.create(
                user = user,
                content_type=c_type,
                object_id=instance.id,
                ip_address = get_client_ip(request)
        )


object_viewed_signal.connect(object_viewed_receiver)


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='comnt_user', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    reply = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    repo = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='snippets')
    media = models.FileField(upload_to=get_comment_upload_path, blank=True, null=True)
    comment_date = models.DateTimeField(default=timezone.now)
    ip_address = models.CharField(max_length=220, blank=True, null=True) #IP Field
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='cont_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    hidden = models.BooleanField(default=False)
    hidden_by = models.ForeignKey(get_user_model(), related_name='comnt_who_hid', on_delete=models.CASCADE, null=True, blank=True)
    date_hidden = models.DateTimeField(null=True, blank=True)
    likes = GenericRelation('Like')
    reports = GenericRelation(Report)
    replies = GenericRelation('self')
    notifications = GenericRelation(Notification)
    class Meta:
        verbose_name_plural = "comments"


class Review(models.Model):
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_review')
    ip_address = models.CharField(max_length=220, blank=True, null=True) #IP Field
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='rcont_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    review_text=models.TextField()
    rating = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.rating


class Offer(models.Model):
    offerer = models.ForeignKey(get_user_model(), related_name='offer_user', on_delete=models.CASCADE)
    offer_price = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    offer_message = models.TextField(blank=True, null=True)
    full_names = models.CharField(blank=True, null=True, max_length=100)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=100)
    ip_address = models.CharField(max_length=220, blank=True, null=True) #IP Field
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='offer_cont_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    location = models.CharField(max_length=255, blank=True, null=True)
    offer_date = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    sender 		= models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='message_sender')
    receiver 	= models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='message_receiver')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=100, blank=True)
    reply 		= models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='m_replies')
    note = models.CharField(max_length=200, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='cont_cont_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.name


class Tag(BaseModel):
    title       = models.CharField(max_length=120)
    slug        = AutoSlugField(populate_from='title', unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='tag_cont_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance
    views = models.IntegerField(default=0)
    active      = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)


class Like(BaseModel):
    user=models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_like')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='lcont_type') # User, Product, Order, Cart, Address
    object_id = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object = GenericForeignKey('content_type', 'object_id') # Product instance

    class Meta:
        verbose_name_plural='Likes'


