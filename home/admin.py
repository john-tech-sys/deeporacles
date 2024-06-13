from django.contrib import admin
from .models import *
# Register your models here.


class UpdateAdmin(admin.ModelAdmin):
    search_fields = ['content', 'slug']
    list_display = ['user', 'slug', 'active', 'hidden',]
    list_editable =  [ 'active', 'hidden']
    list_per_page = 20
    class Meta:
        model = Update
class PostAdmin(admin.ModelAdmin):
    search_fields = ['content', 'meta_keywords', 'meta_description']
    list_display = ['user', 'title', 'active', 'hidden', 'edited']
    list_editable =  [ 'active', 'hidden']
    list_per_page = 20
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)

admin.site.register(Update, UpdateAdmin)


admin.site.register(PostView)
admin.site.register(Space)
admin.site.register(Share)
admin.site.register(PostFiles)
admin.site.register(Savedpost)