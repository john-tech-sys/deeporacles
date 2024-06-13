from django.contrib import admin
from .models import *
# Register your models here.



class FaqAdmin(admin.ModelAdmin):
    class Meta:
        model = Faq
        fields = {'title', 'active', 'edited'}


class HelpAdmin(admin.ModelAdmin):
    class Meta:
        model = Help
        fields = {'title', 'description', 'active', 'edited'}


class StartsellingAdmin(admin.ModelAdmin):
    class Meta:
        model = Help
        fields = {'title', 'active'}

class SafetyTipsAdmin(admin.ModelAdmin):
    class Meta:
        model = SafetyTips
        fields = {'title', 'active', 'edited'}


class TermsAdmin(admin.ModelAdmin):
    class Meta:
        model = Terms
        fields = {'title', 'active', 'edited'}

class PrivacyAdmin(admin.ModelAdmin):
    class Meta:
        model = Privacy
        fields = {'title', 'active', 'edited'}

admin.site.register(SafetyTips, SafetyTipsAdmin)
admin.site.register(Terms, TermsAdmin)
admin.site.register(Privacy, PrivacyAdmin)

admin.site.register(Faq, FaqAdmin)
admin.site.register(Help, HelpAdmin)
admin.site.register(Startselling, StartsellingAdmin)