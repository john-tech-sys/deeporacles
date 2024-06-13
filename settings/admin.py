from django.contrib import admin
from .models import *
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, EmailConfig, Feature

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(EmailConfig, SingletonModelAdmin)
admin.site.register(Feature, SingletonModelAdmin)

# siteinfo = SiteConfiguration.objects.get()
# admin.site.site_header = str(siteinfo.name)

class SlideInline(admin.TabularInline):
    model = Slide
    readonly_fields = ['image_tag']
    extra = 0

class SliderAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_per_page = 10
    inlines = [SlideInline]
    class Media:
        css = {'all': ('no-delete.css',)}
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Slide Setting', {
            'classes': ('collapse', 'open'),
            'fields': ('speed', 'autoplay','autoplay_timeout', 'arrows'),
        }),
    )
admin.site.register(Slider, SliderAdmin)


class FooterlinkAdmin(admin.ModelAdmin):
    list_display = ['section_name']
    list_per_page = 10
    class meta:
        model = FooterLinks
admin.site.register(FooterLinks, FooterlinkAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'active', 'image_tag']
    list_per_page = 10
admin.site.register(Banner, BannerAdmin)

admin.site.register(Confsettings)
admin.site.register(Pages)
admin.site.register(Currency)
admin.site.register(Settings)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Links)