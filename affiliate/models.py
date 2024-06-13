from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class AffiliateLink(models.Model):
    name = models.CharField(max_length=255, help_text='The name of the affiliate link')
    url = models.URLField(max_length=2000, help_text='The URL of the affiliate link')
    affiliate = models.ForeignKey('Affiliate', on_delete=models.CASCADE, help_text='The affiliate that the link is for')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text='The user that the affiliate is for')
    clicks = models.IntegerField(default=0, help_text='The number of times the link has been clicked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Affiliate(models.Model):
    name = models.CharField(max_length=255, help_text='The name of the affiliate')
    code = models.CharField(max_length=255, unique=True, help_text='The unique code for the affiliate')
    description = models.TextField(help_text='A description of the affiliate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

