

from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .account_views import UserViewset


# accounts

acc_router = DefaultRouter()
acc_router.register('account/users', UserViewset)

# profiles

urlpatterns = [
    # accounts
    path('', include(acc_router.urls)),
    path('account/obtain_token', obtain_auth_token, name='obtain_token'),

]

