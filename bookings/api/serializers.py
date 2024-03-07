from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking

User = get_user_model()

class BookingUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'photo',
            'email',
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
            'booking_split_at',

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
        ]

class ListBookingSerializer(serializers.ModelSerializer):
    client = BookingUserSerializer(many=False)
    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'client',
            'service_type',

            'booking_date',
            'booking_time',




        ]
