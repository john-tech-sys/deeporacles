from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import UserRegisterForm, UserUpdateForm
from .models import UserSession


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_admin', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    list_filter = ['is_admin', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    filter_horizontal = ()
    fieldsets = ()
    
    list_per_page = 20
    class meta:
        model = User



admin.site.register(EmailActivation)

admin.site.register(User, CustomUserAdmin)

admin.site.register(EmailConfirmed)

admin.site.register(UserSession)

admin.site.register(Verified)