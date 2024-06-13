from django.urls import path
from .views import mypal

urlpatterns = [
    path('create/', mypal, name='mypal'),
]
