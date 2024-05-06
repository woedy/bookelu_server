from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import Shop, ShopService, ShopInterior, ShopExterior, ShopWork, ShopStaff, ShopPackage, \
    ShopAvailability

User = get_user_model()


class ShopPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPackage
        fields = [
            'id',
            'package_name',
            'price',
            'rating',
            'photo'
        ]

class ShopServiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            #'price',
            #'duration',
            'description',
        ]

class ShopServiceSerializer(serializers.ModelSerializer):
    package_service = ShopPackageSerializer(many=True)

    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            'package_service'
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
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = ShopStaff
        fields = [
            'staff_id',
            'user_id',
            'staff_name',
            'photo',
            'role',
            'rating',
        ]

    def get_user_id(self, obj):
        return obj.user.user_id if obj.user else None

class ShopDetailSerializer(serializers.ModelSerializer):
    shop_services = ShopServiceSerializer(many=True)
    shop_interior = ShopInteriorSerializer(many=True)
    shop_exterior = ShopExteriorSerializer(many=True)
    shop_work = ShopWorkSerializer(many=True)
    shop_staffs = ShopStaffSerializer(many=True)
    #shop_packages = ShopPackageSerializer(many=True)

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
            'rating',
            'open',

            'shop_services',
            'shop_interior',
            'shop_exterior',
            'shop_work',
            'shop_staffs',
            #'shop_packages',

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



class ShopAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAvailability
        fields = '__all__'