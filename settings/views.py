from django.shortcuts import render

# Create your views here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from accounts.models import User
from .models import Settings
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


@receiver(post_save, sender=User)
def create_settings(sender, created, instance, **kwargs):
    if created:
        # only runs if a new User is created
        Settings.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_settings(sender, instance, **kwargs):
    if hasattr(instance, 'settings'):
        instance.settings.save()

class SettingsViewSet(ModelViewSet):
    model = Settings
    serializer_class = SettingsSerializer
    queryset = Settings.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super().create(request, *args, **kwargs)
        return Response({'success': True, 'settings': response.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super().update(request, *args, **kwargs)
        return Response({'success': True, 'settings': response.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super().destroy(request, *args, **kwargs)
        return Response({'success': True}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super().retrieve(request, *args, **kwargs)
        return Response({'success': True, "settings": response.data}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        adds operation success boolean for client
        """
        response = super().list(request, *args, **kwargs)
        return Response({'success': True, 'settings': response.data}, status=status.HTTP_200_OK)


class ChangeSettings(APIView):
    """
        handles changing settings for user
    """
    serializer_class = ConfsettingsSerializer

    def post(self, request):
        if request.data['setting'] == 'private_mode':
            self.change_private_mode(request.user, request.data['value'])
        elif request.data['setting'] == 'night_mode':
            self.change_appearance(request.user, request.data['value'])
        elif request.data['setting'] == 'notifications':
            self.change_notifications(request.user, request.data['value'])
        elif request.data['setting'] == 'save_notifications':
            self.change_save_notifications(request.user, request.data['value'])
        else:
            return Response({'success': False, 'error': 'setting not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(instance=request.user.Confsettings)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    def change_appearance(self, user, value):
        user.Confsettings.night_mode = value
        user.Confsettings.save()

    def change_private_mode(self, user, value):
        user.Confsettings.private_mode = value
        user.Confsettings.save()

    def change_notifications(self, user, value):
        user.Confsettings.notifications = value
        user.Confsettings.save()

    def change_save_notifications(self, user, value):
        user.Confsettings.save_notifications = value
        user.Confsettings.save()
