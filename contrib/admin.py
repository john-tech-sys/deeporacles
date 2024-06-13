from django.contrib import admin
from .models import *
# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    list_filter = ['when']
    list_per_page = 20
    list_display = ['receiver', 'content_type', 'when']
    search_fields = ['receiver__username',]

    class Meta:
        model = Notification

class SearchTermAdmin(admin.ModelAdmin): 
    list_display = ('__unicode__','ip_address','search_date') 
    list_filter = ('ip_address', 'user', 'q') 
    exclude = ('user',) 

class SearchAdmin(admin.ModelAdmin): 
    list_display = ('content_object','date') 

class ReviewAdmin(admin.ModelAdmin):
    list_display=('user','content_type','content_object','review_text','get_review_rating')
    class meta:
        model = Review

class OfferAdmin(admin.ModelAdmin):
    date_hierarchy = 'offer_date'
    list_display = ['offerer', 'content_type', 'content_object', 'offer_price', 'location', 'phone', 'email', 'offer_date']
    list_per_page = 20
    list_filter = ['content_type', 'offer_price', 'location']
    class meta:
        model = Offer

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'comment_date'
    list_display = ['user', 'content_type', 'content_object', 'comment_date']
    list_per_page = 20
    list_filter = [ 'comment_date']
    class meta:
        model = Comment

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'message', 'note']
    list_filter = ['status', 'created_at']

admin.site.register(Message, MessageAdmin)


admin.site.register(Review,ReviewAdmin)
admin.site.register(SearchTerm, SearchTermAdmin)

admin.site.register(Search, SearchAdmin)

admin.site.register(Report)

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Offer, OfferAdmin)

admin.site.register(ObjectViewed)

admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)