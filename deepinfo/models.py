from django.db.models.fields.related import ManyToManyField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from autoslug import AutoSlugField

# Create your models here.


class DeepOracles(models.Model):
    logo_1 = models.ImageField(upload_to='deeporacles', default=None, null=True)
    logo_1_caption = models.CharField(max_length=200, blank=True, null=True)
    logo_2 = models.ImageField(upload_to='deeporacles', default=None, null=True)
    logo_2_caption = models.CharField(max_length=200, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)

    class Meta:
        verbose_name_plural='DeepOracles'

class Deepoo(models.Model):
    logo_1 = models.ImageField(upload_to='deepoo', default=None, null=True)
    logo_1_caption = models.CharField(max_length=200, blank=True, null=True)
    logo_2 = models.ImageField(upload_to='deepoo', default=None, null=True)
    logo_2_caption = models.CharField(max_length=200, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)


class Admin_Message(models.Model):
    sender 		= models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='admin')
    receiver 	= models.ManyToManyField(get_user_model(), related_name='admin_message_receivers')
    content = models.CharField(null=True, blank=True, max_length=255)
    details = FroalaField('Details', blank=True, null=True)
    date 		= models.DateTimeField(auto_now_add=True)
    is_seen		= models.BooleanField(default=False)


class Aboutus(models.Model):
	line1 = models.CharField(max_length=250)
	line2 = models.TextField()
	line3 = models.TextField()
	banner = models.ImageField(upload_to='aboutus/banner')

	class Meta:
		verbose_name_plural='Aboutus'
		
	def ImageUrl(self):
		if self.banner:
			return self.banner.url
		else:
			return ""

	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.banner.url))
	image_tag.short_description = 'Image'

	def __str__(self):
		return self.line1
	

class TeamInfo(models.Model):
	name = models.CharField(max_length=250)
	job_title = models.CharField(max_length=250)
	email = models.EmailField()
	image = models.ImageField(upload_to = 'aboutus/team/')
	about_us = models.ForeignKey(Aboutus, on_delete = models.CASCADE)

	def __str__(self):
		return self.name
	

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""
	
	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'