from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status

from bookings.api.serializers import ListBookingSerializer, BookingSerializer
from bookings.models import Booking
from shop.models import Shop


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_bookings_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    bookings = []


    shop_id = request.query_params.get('shop_id', None)

    if not shop_id:
        errors['shop_id'] = ['Shop ID is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)




    _bookings = Booking.objects.filter(shop=shop).order_by('-created_at')
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        bookings = booking_serializer.data

    data['bookings'] = bookings




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_booking_detail_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}



    booking_id = request.query_params.get('booking_id', None)

    if not booking_id:
        errors['booking_id'] = ['Booking ID is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)




    booking_serializer = BookingSerializer(booking, many=False)
    if booking_serializer:
        booking_detail = booking_serializer.data






    payload['message'] = "Successful"
    payload['data'] = booking_detail

    return Response(payload, status=status.HTTP_200_OK)
