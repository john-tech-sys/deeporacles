
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from froala_editor.fields import FroalaField


# Create your models here.


class Info(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to='noticeboard/info', null=True, blank=True)
    image_caption = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField('Description', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    highlight = models.TextField('Highlight', max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True )
    date_posted = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)
    

    def get_absolute_url(self):
        return reverse("info",  kwargs={"pk": self.pk})


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Startselling(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    details = FroalaField('Details', blank=True, null=True)
    highlight = models.TextField('Highlight', max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)
    
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Faq(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    drop_cap = models.CharField(max_length=10, null=True, blank=True)
    highlight = models.TextField('Highlight', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Help(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    drop_cap = models.CharField(max_length=10, null=True, blank=True)
    highlight = models.TextField('Highlight', max_length=200, blank=True, null=True)
    description = models.TextField('Brief Description', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True )
    active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)

    class Meta:
        verbose_name_plural='Help'


    def get_absolute_url(self):
        return reverse("info",  kwargs={"pk": self.pk})


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class NewsCategory(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='noticeboard/newscategory', null=True, blank=True)
    slug = models.SlugField( max_length=255, unique=True)
    active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)
    
    class Meta:
        verbose_name_plural='NewsCategories'
        
    def get_absolute_url(self): 
        return reverse('category', kwargs={ "category_slug": self.slug })

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey("NewsCategory",blank=True, null=True, related_name='infocategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to='noticeboard/news', null=True, blank=True)
    image_caption = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField('Description', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True )
    date_posted = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', null=True, blank=True) 
    meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', null=True, blank=True)
    
    class Meta:
        ordering = ('-date_posted',)
        verbose_name_plural='News'


    def get_absolute_url(self):
        return reverse("info",  kwargs={"pk": self.pk})


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Privacy(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField('Brief Description', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True )
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural='Privacies'
        
    def get_absolute_url(self):
        return reverse("info",  kwargs={"pk": self.pk})


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Terms(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField('Brief Description', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural='Terms'


    def get_absolute_url(self):
        return reverse("info",  kwargs={"pk": self.pk})


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Security(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField('Brief Description', max_length=200, blank=True, null=True)
    details = FroalaField('Details', blank=True, null=True)
    slug = models.SlugField(max_length=150, blank=True, null=True )
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural='Securities'
        
    def get_absolute_url(self):
        return reverse("info",  kwargs={"pk": self.pk})


    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class SafetyTips(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    details = FroalaField('Details', blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural='SafetyTips'
        
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class NewsletterEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)


class Newsletter(models.Model):
    # # use this arrayfield only with postgress database else it will cause an error

    # emails = ArrayField(
    #     ArrayField(
    #         models.EmailField(blank=True), null=True
    #     ), null=True
    # )
    subject = models.TextField()
    body = FroalaField('Body', blank=True, null=True)
    send_date = models.DateTimeField(default=timezone.now)

    # def total_email(self):
    #     return len(self.emails)
