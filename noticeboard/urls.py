from django.contrib import admin
from django.urls import path
from . import views as board_views

# app_name = 'noticeboard'

urlpatterns = [
    path('faq', board_views.faq, name='faq'),
    path('startselling', board_views.startselling, name='startselling'),
    path('safetytips', board_views.safetytips, name='safetytips'),
    path('terms', board_views.terms, name='terms'),
]