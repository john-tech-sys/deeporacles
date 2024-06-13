

from django.db import router
from django.urls import path, include
from .profile_views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# profiles

prof_router = DefaultRouter()
prof_router.register('profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    # profiles

    path('', include(prof_router.urls)),

    path('my_posts', my_posts, name='my_posts'),  

    path('updates', updates, name='updates'),

    path('create_story', create_status_view, name="create_story"),

    path('saved_posts', saved_posts, name='saved_posts'),

    path('user_posts/<int:pk>/', user_posts, name='user_posts'),

    path("addressbook/<int:id>", AddressBookDetails.as_view()),
    # connections
]

