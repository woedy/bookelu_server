from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate

from admin_app.api.serializers import ListAdminShopsSerializer
from bookings.models import Booking
from shop.models import Shop

User = get_user_model()

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def overview_view(request):
    payload = {}
    data = {}
    errors = {}

    vendors_count = 0
    all_users_count = 0
    all_appointments_count = 0
    stats_data = {}

    all_shops = Shop.objects.all()
    vendors_count = all_shops.count()

    all_users = User.objects.all().filter(user_type="Client")
    all_users_count = all_users.count()

    all_bookings = Booking.objects.all()
    all_appointments_count = all_bookings.count()


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    data['vendors_count'] = vendors_count
    data['all_users_count'] = all_users_count
    data['all_appointments_count'] = all_appointments_count
    data['stats_data'] = stats_data





    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_shops_admin_view(request):
    payload = {}
    data = {}
    errors = {}


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    shops = Shop.objects.all()

    shops_serializer = ListAdminShopsSerializer(shops, many=True)
    if shops_serializer:
        _shops = shops_serializer.data
        data['shops'] = _shops

    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)



