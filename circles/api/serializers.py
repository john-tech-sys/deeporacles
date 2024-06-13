

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from circles.models import Circles
from profiles.models import (AddressBook, Profile, ProfilePic, Skill, Education,
                            Potfolio, Files)
from accounts.models import User
from settings.models import Area, City, Region


# accounts

class CirclesSerializer(serializers.ModelSerializer):
    """
    used to serializer circles model
    """
    private_mode = serializers.BooleanField(source='settings.private_mode', required=False, read_only=True)
    class Meta:
        model = Circles
        fields = ('id', 'user', 'followers', 'following', 'connections', 'forums')
        extra_kwargs = {
            'connections': {'required': False},
            'user': {'required': False},
        }
    def validate(self, attrs):
        if self.instance in attrs.get('connections', []):
            raise serializers.ValidationError('you cannot connect with yourself')
        return attrs
