from django.contrib import admin
from .models import *
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'phone', 'date_joined']
    list_filter = ['date_joined']
    search_fields = ['user', 'first_name', 'last_name', 'email']
    list_per_page = 20
    # form = ProfileUpdateForm
    # form = UserUpdateForm
    class meta:
        model = Profile

admin.site.register(ProfilePic)
admin.site.register(AddressBook)
admin.site.register(Files)
admin.site.register(Education)
admin.site.register(Potfolio)
admin.site.register(Skill)
admin.site.register(Profile, ProfileAdmin)