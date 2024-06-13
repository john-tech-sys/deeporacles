

from rest_framework import serializers
from accounts.models import User


# accounts

class UserSerializer(serializers.ModelSerializer):
    """
    used to serialize user model
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'date_joined', 'last_name','password', 'first_name')
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
            "email": {"write_only": True,},
            "last_name": {"required": False},
            "date_joined": {"read_only": True, "required": False},
            "first_name": {"required": False},
        }
    def validate(self,attrs):
        email_exists = User.objects.filter(username=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError(details="User with this Email exists")
        return super().validate(attrs)


# profiles
