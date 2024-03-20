from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate

from activities.models import AllActivity
from admin_app.api.serializers import ListAdminShopsSerializer, ListAdminAllUsersSerializer, AdminUserDetailSerializer
from bookings.models import Booking
from shop.api.serializers import ShopDetailSerializer
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


    shops = Shop.objects.all().filter(registration_complete=True)

    shops_serializer = ListAdminShopsSerializer(shops, many=True)
    if shops_serializer:
        _shops = shops_serializer.data
        data['shops'] = _shops

    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def admin_shop_details_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.query_params.get('shop_id', None)

    if not shop_id:
        errors['shop_id'] = ["Shop id required"]

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        errors['shop_id'] = ['Shop does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shop_detail = Shop.objects.get(shop_id=shop_id)

    shop_detail_serializer = ShopDetailSerializer(shop_detail, many=False)
    if shop_detail_serializer:
        _shop = shop_detail_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _shop

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_vendor_view(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        shop_id = request.data.get('shop_id', "")


        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except:
            errors['shop_id'] = ['Shop does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        shop.is_deleted = True
        shop.save()

        shop.user.is_deleted = True
        shop.user.save()
        shop.save()

        new_activity = AllActivity.objects.create(
            user=shop.user,
            subject="Shop Removed",
            body="Admin Just deleted shop. " + shop.shop_name
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_users_admin_view(request):
    payload = {}
    data = {}
    errors = {}


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    all_users = User.objects.all().filter(is_deleted=True)

    users_serializer = ListAdminAllUsersSerializer(all_users, many=True)
    if users_serializer:
        _users = users_serializer.data
        data['all_users'] = _users

    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def admin_user_details_view(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.query_params.get('user_id', None)

    if not user_id:
        errors['user_id'] = ["User id required"]

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    user_detail = User.objects.get(user_id=user_id)

    user_detail_serializer = AdminUserDetailSerializer(user_detail, many=False)
    if user_detail_serializer:
        _user = user_detail_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _user

    return Response(payload, status=status.HTTP_200_OK)


