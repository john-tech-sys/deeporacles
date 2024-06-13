from django.contrib import admin
from .models import Affiliate, AffiliateLink
# Register your models here.

admin.site.register(AffiliateLink)
admin.site.register(Affiliate)