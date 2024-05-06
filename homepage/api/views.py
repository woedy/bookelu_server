
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from bookings.api.serializers import BookingSerializer, ListBookingSerializer
from bookings.models import Booking
from shop.api.serializers import ShopServiceSerializer, ShopStaffSerializer
from shop.models import Shop, ShopService, ShopStaff

User = get_user_model()

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_homepage_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    shop_info = {}
    bookings_today = []
    shop_categories = []
    shop_staffs = []


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


    shop_info['shop_name'] = shop.shop_name
    shop_info['location_name'] = shop.location_name

    service = ShopService.objects.filter(shop=shop)
    service_serializer = ShopServiceSerializer(service, many=True)
    if service_serializer:
        shop_categories = service_serializer.data

    staff = ShopStaff.objects.filter(shop=shop)
    staff_serializer = ShopStaffSerializer(staff, many=True)
    if staff_serializer:
        shop_staffs = staff_serializer.data

    _bookings = Booking.objects.filter(shop=shop).order_by('-created_at')
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        bookings_today = booking_serializer.data

    data['shop_info'] = shop_info
    data['bookings_today'] = bookings_today
    data['shop_categories'] = shop_categories
    data['shop_staffs'] = shop_staffs




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def client_homepage_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    shop_info = {}
    bookings_today = []
    shop_categories = []
    shop_staffs = []
    promotions = []


    promotion = {
        "title": "Black Friday",
        "package_name": "Well Dress Rasta",
        "original_price": "$3000",
        "promo_price": "$2000",
        "status": "Available",
        "photo": "package_image.png"
    }

    promotions.append(promotion)

    user_id = request.query_params.get('user_id', None)

    if not user_id:
        errors['user_id'] = ['User ID is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    _bookings = Booking.objects.filter(client=user).order_by('-created_at')
    booking_serializer = ListBookingSerializer(_bookings, many=True)
    if booking_serializer:
        bookings_today = booking_serializer.data

    data['bookings'] = bookings_today
    data['promotions'] = promotions




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





