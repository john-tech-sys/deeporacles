

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from contrib.models import Offer, Review


class ModelSerializer(serializers.ModelSerializer):
    def get_requet_method_type(self):
        request = self.context.get("request")
        return request.method


class OfferSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField()
    class Meta:
        model = Offer
        fields = [
            'offerer', 'offer_price', 'offer_message', 'full_names', 'phone', 'email', 'location', 'offer_date'
        ]

class ReviewSerializer(serializers.ModelSerializer):
	user = serializers.CurrentUserDefault()
	class Meta:
		model = Review
		fields = '__all__'

# service

