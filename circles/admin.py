

from django.contrib import admin
from .models import Forum, Circles


class CirclesAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user',]

    class Meta:
        model = Circles


admin.site.register(Circles, CirclesAdmin)

# Register your models here.
admin.site.register(Forum)
