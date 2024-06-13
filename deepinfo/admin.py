from django.contrib import admin
from .models import *
# Register your models here.

class DeepOraclesAdmin(admin.ModelAdmin):
    class Meta:
        model = DeepOracles
        fields = {'meta_keywords', 'meta_description'}

class TeamInfoInline(admin.TabularInline):
    model = TeamInfo
    readonly_fields = ['image_tag']
    extra = 3

class AboutusAdmin(admin.ModelAdmin):
    list_display = ['line1', 'image_tag']
    inlines = [TeamInfoInline]
admin.site.register(Aboutus, AboutusAdmin)

class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'job_title', 'image_tag']
admin.site.register(TeamInfo, TeamInfoAdmin)


admin.site.register(DeepOracles, DeepOraclesAdmin)

admin.site.register(Admin_Message)

admin.site.register(Deepoo)