from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking, BookingPayment, BookingRating
from shop.models import ShopService, Shop, ShopStaff, ShopPackage
from user_profile.models import UserProfile

User = get_user_model()

class BookingRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRating
        fields = [
            'id',
            'rating',
            'report',

        ]

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'shop_name',
            'photo',

        ]



class BookingPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = [
            'id',
            'payment_method',
            'amount',
        ]
class BookingPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopPackage
        fields = [
            'id',
            'package_name',
            'photo',
            'price',
            'rating',
        ]



class BookingSeriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            'price',
        ]


class BookingStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopStaff
        fields = [
            'staff_id',
            'staff_name',
            'role',
            'photo',
            'rating',
        ]


class BookingUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'photo',
            'phone',
        ]

class BookingUserSerializer(serializers.ModelSerializer):
    personal_info = BookingUserProfileSerializer(many=False)
    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'full_name',
            'personal_info',
        ]


class BookingSerializer(serializers.ModelSerializer):
    client = BookingUserSerializer(many=False)
    service = BookingSeriveSerializer(many=False)
    booked_staff = BookingStaffSerializer(many=False)
    package = BookingPackageSerializer(many=False)
    booking_payments = BookingPaymentsSerializer(many=False)
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'shop',
            'service',
            'client',
            'service_type',
            'package',
            'booked_staff',

            'booking_date',
            'booking_time',

            're_scheduled',
            'booking_rescheduled_at',

            'confirm_payment',

            'split',
            'booking_split_from',
            'booking_split_to',

            'amount_to_pay',
            'actual_price',

            'actual_duration',
            'notes',
            'review',

            'status',
            'booking_start',
            'booking_end',
            'booking_approved_at',
            'booking_declined_at',
            'booking_cancelled_at',
            'booking_payments'
        ]

class ListBookingSerializer(serializers.ModelSerializer):
    client = BookingUserSerializer(many=False)
    service = BookingSeriveSerializer(many=False)
    package = BookingPackageSerializer(many=False)
    booked_staff = BookingStaffSerializer(many=False)
    booking_payments = BookingPaymentsSerializer(many=False)
    shop = ShopSerializer(many=False)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client',
            'service_type',
            'service',
            'shop',
            'package',

            'booking_date',
            'booking_time',
            'status',

            'booking_payments',
            "booked_staff"

        ]



class ListBookingAdminSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    price = serializers.CharField(source='amount_to_pay')

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client_name',
            'shop_name',
            'price',
            'status'
        ]

    def get_client_name(self, obj):
        return obj.client.full_name if obj.client else None

    def get_shop_name(self, obj):
        return obj.shop.shop_name if obj.shop else None