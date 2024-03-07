from django.contrib.auth import get_user_model
from rest_framework import serializers

from shop.models import Shop


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



