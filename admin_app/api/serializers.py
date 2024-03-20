from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookelu_project import settings
from shop.models import Shop
from user_profile.models import UserProfile

User = settings.AUTH_USER_MODEL

class ListAdminShopsSerializer(serializers.ModelSerializer):
    services_count = serializers.SerializerMethodField()
    staffs_count = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = [
            'shop_id',
            'shop_name',
            'photo',
            'services_count',
            'staffs_count'
        ]

    def get_services_count(self, obj):
        return obj.shop_services.count()

    def get_staffs_count(self, obj):
        return obj.shop_staffs.count()

class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = [
            'phone',
            'photo',

        ]

class ListAdminAllUsersSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(many=False)
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',

            'user_profile'

        ]


class AdminUserDetailSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(many=False)
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',

            'user_profile'

        ]

