from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from solo.models import SingletonModel
from django.contrib.auth import get_user_model
# Create your models here.



class Confsettings(models.Model):
    theme_choices = (
        (True, "use dark theme"),
        (False, "white-content")
    )

    private_mode_choices = (
        (True, "other contacts cannot add you to a conversation"),
        (False, "other contacts can add you to a conversation"),
    )

    notifications_choices = (
        (True, 'receive notifications'),
        (False, 'never receive notifications')
    )
    save_notifications_choices = (
        (True, 'save notifications'),
        (False, 'delete notifications')
    )
    night_mode = models.BooleanField(max_length=10, default=True, choices=theme_choices)
    private_mode = models.BooleanField(default=False, choices=private_mode_choices)
    notifications = models.BooleanField(default=True, choices=notifications_choices)
    save_notifications = models.BooleanField(default=False, choices=save_notifications_choices)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)


BANNER_TYPE = (
	('banner1', 'banner1'),
	('banner2', 'banner2'),
	('banner3', 'banner3'),
	('banner4', 'banner4'),
	('banner5', 'banner5'),
	('banner6', 'banner6'),
	('banner4', 'banner7'),
	('banner8', 'banner8'),
)

class Banner(models.Model):
	title = models.CharField(max_length=100)
	caption1 = models.CharField(max_length=500, blank=True, null=True)
	caption2 = models.CharField(max_length=500, blank=True, null=True)
	caption3 = models.CharField(max_length=500, blank=True, null=True)
	call_to_text = models.CharField(max_length=500, default="Shop Now")
	call_to_url = models.CharField(max_length=500, default="/")
	image = models.ImageField(upload_to = 'banner/')
	banner_type = models.CharField(max_length=50, default='Top', choices=BANNER_TYPE)
	active = models.BooleanField(default=True)

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""
	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'

	def __str__(self):
		return self.title

class Slider(models.Model):
	name = models.CharField(max_length=250)
	speed = models.IntegerField(default=3000)
	autoplay = models.BooleanField(default=True)
	autoplay_timeout = models.IntegerField(default=4000)
	dots = models.BooleanField(default=True)
	arrows = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def slides(self):
		return Slide.objects.filter(slider = self).order_by("position")
	
	class Meta:
		verbose_name = 'Slider'

class Slide(models.Model):
	slider = models.ForeignKey(Slider, on_delete = models.CASCADE, related_name="slide")
	caption_1 = models.CharField( max_length=250, verbose_name='caption 1')
	caption_2 = models.CharField( max_length=250, verbose_name='caption 2')
	caption_3 = models.CharField( max_length=250, verbose_name='caption 3')
	action_text = models.CharField( max_length=200, verbose_name='Call to Action Text')
	action_url = models.URLField(verbose_name='Call to Action URL')
	link_type = models.BooleanField(verbose_name='Open in new window')
	image = models.ImageField(upload_to = 'slide/')
	active = models.BooleanField(verbose_name='Status')
	position = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return ''
	

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""

	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'


class Pages(models.Model):
	name = models.CharField(max_length=500)
	body = models.TextField()
	active = models.BooleanField(default=True)
	slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)

	def __str__(self):
		return self.name

@receiver(pre_save, sender=Pages)
def populate_slug(sender, instance, **kwargs):
	instance.slug = slugify(instance.name)

class SiteConfiguration(SingletonModel):
	name = models.CharField(max_length=255, default='Deep Oracles')
	privacy_policy = models.ForeignKey(Pages, on_delete=models.DO_NOTHING, related_name='privacy_policy', blank=True, null=True)
	term_condition = models.ForeignKey(Pages, on_delete=models.DO_NOTHING, related_name='term_condition', blank=True, null=True)
	phone = models.CharField(max_length=20, default = 1, blank=True, null=True)
	logo = models.ImageField(upload_to='settings/', default = 'default/bitmagus.png')
	address=models.CharField(max_length=200, default = 'Kampala')
	email = models.EmailField(blank=True, null=True)
	twitter = models.URLField(default = 'twitter.com')
	facebook = models.URLField(default = 'facebook.com')
	youtube = models.URLField(default = 'youtube.com')
	instagram = models.URLField(default = 'instagram.com')
	favicon = models.ImageField(upload_to='settings/',  default = 'default/bitmagus.png')
	slider = models.ForeignKey(Slider, on_delete = models.DO_NOTHING, blank=True, null=True)
	banner1 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner1')
	banner2 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner2')
	banner3 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner3')
	banner4 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner4')
	banner5 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner5')
	banner6 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner6')
	banner7 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner7')
	banner8 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner8')
	maintenance_mode = models.BooleanField(default=False)

	def __str__(self):
		return "Site Configuration"

	class Meta:
		verbose_name = "Site Configuration"

class Links(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	link = models.URLField()

	def __str__(self):
		return self.name

class FooterLinks(models.Model):
	active = models.BooleanField(default=True)
	is_footer = models.BooleanField(default=False)
	section_name = models.CharField(max_length=200)
	icon = models.CharField(max_length=50, blank=True, null=True)
	links = models.ManyToManyField(Links)

class Currency(models.Model):
	symbol = models.CharField(max_length=10)
	name = models.CharField(max_length=100)
	symbol_native = models.CharField(max_length=5)
	rate = models.FloatField(default=1)
	decimal_digits = models.CharField(max_length=2)
	code = models.CharField(max_length=10)
	name_plural = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	default = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Settings(models.Model):
	default_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='defailt_currency')
	supported_currency = models.ManyToManyField(Currency, related_name='supported_currency')
	welcome_email = models.BooleanField(default=True)
	order_email = models.BooleanField(default=True)
	order_status_email = models.BooleanField(default=True)
	invoice_email = models.BooleanField(default=True)

class EmailConfig(SingletonModel):
	email_host = models.CharField(max_length=200)
	email_port = models.CharField(max_length=20)
	email_use = models.CharField(max_length=10)
	email_host_user = models.CharField(max_length=100)
	email_host_password = models.CharField(max_length=50)

class Feature(SingletonModel):
	title1 = models.CharField(max_length=300, blank=True, null=True)
	subtitle1 = models.CharField(max_length=300, blank=True, null=True)
	icon1 = models.CharField(max_length=100, blank=True, null=True)
	title2 = models.CharField(max_length=300, blank=True, null=True)
	subtitle2 = models.CharField(max_length=300, blank=True, null=True)
	icon2 = models.CharField(max_length=100, blank=True, null=True)
	title3 = models.CharField(max_length=300, blank=True, null=True)
	subtitle3 = models.CharField(max_length=300, blank=True, null=True)
	icon3 = models.CharField(max_length=100, blank=True, null=True)
	title4 = models.CharField(max_length=300, blank=True, null=True)
	subtitle4 = models.CharField(max_length=300, blank=True, null=True)
	icon4 = models.CharField(max_length=100, blank=True, null=True)
 
class Country(models.Model):
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Region(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name = "region")
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class City(models.Model):
	region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, related_name = "city")
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Area(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, related_name = "area")
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name


