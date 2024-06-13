from django.contrib import admin
from django.urls import path
from . import views as ajoinfo_views
from .views import AdminMessageView


urlpatterns = [
    path('about', ajoinfo_views.about, name='about'),
    path('contact', ajoinfo_views.contact, name='contact'),
	path('admin_message', ajoinfo_views.AdminMessageView, name="admin_message"),
	
]