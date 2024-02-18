from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import Shop, ShopService, ShopInterior, ShopExterior, ShopWork, ShopStaff

User = get_user_model()


class ShopServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopService
        fields = [
            'service_type',
        ]

class ShopInteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopInterior
        fields = [
            'photo',
        ]

class ShopExteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopExterior
        fields = [
            'photo',
        ]

class ShopWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopWork
        fields = [
            'photo',
        ]


class ShopStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopStaff
        fields = [
            'staff_name',
            'photo',
            'role',
            'photo',
        ]


class ShopDetailSerializer(serializers.ModelSerializer):
    shop_services = ShopServiceSerializer(many=True)
    shop_interior = ShopStaffSerializer(many=True)
    shop_exterior = ShopWorkSerializer(many=True)
    shop_work = ShopExteriorSerializer(many=True)
    shop_staffs = ShopInteriorSerializer(many=True)

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

            'shop_services',
            'shop_interior',
            'shop_exterior',
            'shop_work',
            'shop_staffs',

        ]



class ListShopsSerializer(serializers.ModelSerializer):
    shop_services = ShopServiceSerializer(many=True)

    class Meta:
        model = Shop
        fields = [
            'shop_id',
            'shop_name',
            'photo',
            'location_name',
            'shop_services'
        ]


