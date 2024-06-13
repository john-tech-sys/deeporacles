from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views


urlpatterns = [

	# notifications

	path('notify/<int:pk>/href', views.NotifyHref, name="notify-href"),

	path('activate/post/<int:pk>/notifies', views.ActivatePostNotify, name='open-post-notifies'),

	path('notification/<int:notification_pk>/post/<int:post_pk>/', views.PostNotification.as_view(), name='post_notification'),

	path('notification/<int:notification_pk>/profile/<int:profile_pk>/', views.ProfileNotification.as_view(), name='profile_notification'),

	path('notification/delete/<int:notification_pk>', views.delete, name='remove_notification'),

	path('view_all_notifications/', views.view_all_notifs, name='view_all_notifs'),
 

]