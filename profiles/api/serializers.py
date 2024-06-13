

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from circles.models import Circles
from profiles.models import (AddressBook, Profile, ProfilePic, Skill, Education,
                            Potfolio, Files)
from settings.models import Area, City, Region


# profiles

class ProfileSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(allow_blank=True, allow_null=True)
    """
    used to serializer profile model
    """
    private_mode = serializers.BooleanField(source='settings.private_mode', required=False, read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'user', 'first_name', 'middle_name', 'last_name', 'picture', 'image', 'gender', 'phone',
            'email', 'birth_date', 'bio', 'slug', 'gender', 'date_joined', 'is_online', 'blocked', 'is_active', 'saved_posts', 'chatted_with',
            'private_mode')


class CirclesSerializer(serializers.ModelSerializer):
    """
    used to serializer circles model
    """
    private_mode = serializers.BooleanField(source='settings.private_mode', required=False, read_only=True)
    class Meta:
        model = Circles
        fields = ('id', 'user', 'followers', 'following', 'favourite_store', 'connections', 'forums')
        extra_kwargs = {
            'connections': {'required': False},
            'user': {'required': False},
        }
    def validate(self, attrs):
        if self.instance in attrs.get('connections', []):
            raise serializers.ValidationError('you cannot connect with yourself')
        return attrs


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePic
        fields = {
            'profile', 'image', 'updated', 'featured', 'active'
        }

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = {
            'profile', 'title', 'image', 'score', 'details', 'is_key_skill', 'is_active'
        }

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = {
            'profile', 'institution', 'qualification', 'period', 'is_highest_level', 'is_active'
        }

class PotfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Potfolio
        fields = {
            'profile', 'title', 'image', 'description', 'details', 'slug', 'is_active'
        }

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = {
            'profile', 'title', 'image', 'document'
        }


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddressBook
		exclude = ['temp', 'user']

class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = City
		fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Area
		fields = '__all__'

