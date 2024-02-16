from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import Shop

User = get_user_model()

class ShopSerializer(serializers.ModelSerializer):


    class Meta:
        model = Shop
        fields = [
            'shop_id',
            'shop_name',
            'email',
            'business_type',
            'country',
            'phone',
            'description',
            'business_days',
            'business_hours_open',
            'business_hours_close',
            'special_features',
            'photo',
            'street_address1',
            'street_address2',
            'city',
            'state',
            'zipcode',
            'location_name',
            'lat',
            'lng',


        ]



