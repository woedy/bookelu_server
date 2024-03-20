from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking, BookingPayment
from shop.models import ShopService
from user_profile.models import UserProfile

User = get_user_model()

class BookingPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingPayment
        fields = [
            'id',
            'payment_method',
            'amount',
        ]
class BookingSeriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopService
        fields = [
            'service_id',
            'service_type',
            'price',
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
    booking_payments = BookingPaymentsSerializer(many=False)
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'shop',
            'service',
            'client',
            'service_type',

            'booking_date',
            'booking_time',

            're_scheduled',
            'booking_rescheduled_at',

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
    booking_payments = BookingPaymentsSerializer(many=False)
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client',
            'service_type',
            'service',

            'booking_date',
            'booking_time',
            'status',

            'booking_payments'

        ]
