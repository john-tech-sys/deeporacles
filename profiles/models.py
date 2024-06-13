
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from deeporacles import settings
from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from froala_editor.fields import FroalaField
from django.core.mail import send_mail
from settings.models import Area, City, Country, Region
DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)


# def get_profile_cover_path(self, filename):
#     	return 'profiles/cover/' + str(self.pk) + filename
def get_profile_cover_path(instance, filename):
	return 'profiles/{0}/{1}'.format(instance.name, filename)

# def get_profile_pic_path(instance, filename):
# 	return 'profiles/{0}/pic/{1}'.format(instance.name, filename)
def get_profile_pic_path(instance, filename):
	return 'profiles/{0}/{1}'.format(instance.name, filename)


class Profile(models.Model):
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(get_user_model(), verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    picture = models.ImageField(default='default/default-avatar.JPG', upload_to=get_profile_pic_path, blank=True, null=True)
    bio = FroalaField('Bio', blank=True, null=True, default = "Hi there! Let's be friends")
    birth_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    image = models.ImageField(default='default/014.jpeg', upload_to=get_profile_pic_path, blank=True, null=True)
    gender = models.CharField(max_length=10, choices = SEX_CHOICES, null =True, blank=True)
    email = models.EmailField(('email address'), unique=True, null=True, blank=True)
    first_login = models.BooleanField(default=False)
    phone = PhoneNumberField(blank=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add = True, blank=True, null=True)
    is_online = models.BooleanField(('online'), default=True)
    blocked = models.ManyToManyField(get_user_model(), blank=True, related_name='user_blocked')
    is_active = models.BooleanField(default=True)
    allow_anonymous = models.BooleanField(default=True)
    chatted_with = models.ManyToManyField(get_user_model(), related_name='user_chatted_with', blank=True)
    private_mode = models.BooleanField(default=True)
    hide_sensitive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    # def online(self):
    #     if self.is_online:
    #         return (timezone.now() - self.is_online) < timezone.timedelta(minutes=1)
    #     return False

    def get_online_info(self):
        if self.is_online == True:
            return 'Online'
        if self.is_online == False:
            return 'Offline'

    def name(self):
        if self.first_name and self.last_name:
            name = '%s %s' % (self.first_name, self.last_name)
        elif self.first_name:
            name = self.first_name
        elif self.last_name:
            name = self.last_name
        if self.user.first_name and self.user.last_name:
            name = '%s %s' % (self.user.first_name, self.user.last_name)
        elif self.user.first_name:
            name = self.user.first_name
        elif self.user.last_name:
            name = self.user.last_name
        else:
            name = self.user
        return name

    def get_short_name(self):
        """Return the short name for the user."""
        if self.first_name:
            get_short_name = self.first_name
        elif self.last_name:
            get_short_name = self.last_name
        elif self.user.first_name:
            get_short_name = self.user.first_name
        elif self.user.last_name:
            get_short_name = self.user.last_name
        else:
            get_short_name = self.user
        return self.first_name

    def name_initials(self):
        if self.first_name and self.last_name:
            name = '%s %s' % (self.first_name[0], self.last_name[0])
        elif self.first_name:
            name = '%s %s' % (self.first_name[0], self.first_name[1])
        elif self.last_name:
            name = '%s %s' % (self.last_name[0], self.last_name[1])
        if self.user.first_name and self.user.last_name:
            name = '%s %s' % (self.user.first_name[0], self.user.last_name[0])
        elif self.user.first_name:
            name = '%s %s' % (self.user.first_name[0], self.user.first_name[1])
        elif self.user.last_name:
            name = '%s %s' % (self.user.last_name[0], self.user.last_name[1])
        else:
            name = '%s %s' % (self.user.username[0], self.user.username[1])
        return name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse("profile_view",  kwargs={"profile_slug": self.slug})

    def imagaURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def profile_email(self, **kwargs):
        if self.email:
            email = self.email
        else:
            email = self.user.email
        return email

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]


class ProfilePic(models.Model):
    profile = models.ForeignKey("Profile", related_name='profilepic', on_delete=models.CASCADE)
    image = models.ImageField(default='default/014.jpeg', upload_to='profile/images', blank=True)
    thumbnail = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.first_name

class Skill(models.Model):
    profile = models.ForeignKey("Profile", related_name='skill', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    details = models.TextField(max_length=500, null=True, blank=True)
    score = models.IntegerField(default=50, blank=True, null=True)
    image = models.ImageField(upload_to='profile/skills', blank=True, null=True)
    is_key_skill = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

class Potfolio(models.Model):
    profile = models.ForeignKey("Profile", related_name='potfolio', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    details = FroalaField('Details', blank=True, null=True)
    image = models.ImageField(upload_to='profile/potfolio', blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    slug = AutoSlugField(populate_from='title', unique=True)
    class Meta:
        verbose_name = 'Potfolio'
        verbose_name_plural = 'Potfolios'
        ordering = ['title']

    def __str__(self):
        return str(self.title)

class Education(models.Model):
    profile = models.ForeignKey("Profile", related_name='education', on_delete=models.CASCADE, blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    period = models.CharField(max_length=30, blank=True, null=True)
    is_highest_level = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.qualification)

class Files(models.Model):
    profile = models.ForeignKey("Profile", related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='profile/files', blank=True, null=True)
    document = models.FileField(upload_to='documents', blank=True, null=True)

    def __str__(self):
        return str(self.title)


class AddressBook(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE, related_name="address_book")
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete = models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete = models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete = models.CASCADE, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete = models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=500)
    default = models.BooleanField(default=True)
    temp = models.BooleanField(default=False)

    def __str__(self):
        return self.name+" ("+self.user.first_name+" "+self.user.last_name+")"

    def get_short_address(self):
        return "{profile} {adress}, {city}".format(
                user = self.user,
                address = self.address,
                city = self.city
            )

    def get_full_address(self):
        return "{user}\n{adress}\n{city}\n{state}, {country}".format(
                user = self.user,
                address = self.address,
                city = self.city,
                region = self.region,
                country = self.country
            )