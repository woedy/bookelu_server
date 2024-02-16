from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.api.serializers import ShopSerializer
from shop.models import Shop, ShopInterior, ShopExterior, ShopWork, ShopService, ShopStaff


# Create your views here.
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([ ])
def add_shop_view(request):
    payload = {}
    data = {}
    errors = {}



    shop_name = request.data.get('shop_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')
    country = request.data.get('country', '')
    street_address1 = request.data.get('street_address1', '')
    street_address2 = request.data.get('street_address2', '')
    city = request.data.get('city', '')
    state = request.data.get('state', '')
    zipcode = request.data.get('zipcode', '')
    location_name = request.data.get('location_name', '')
    location_lat = request.data.get('location_lat', '')
    location_lng = request.data.get('location_lng', '')
    business_type = request.data.get('business_type', '')
    business_logo = request.data.get('business_logo', '')
    password1 = request.data.get('password1', '')
    password2 = request.data.get('password2', '')

    if not shop_name:
        errors['shop_name'] = ["Shop name required"]

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    new_shop = Shop.objects.create(
        email=email,
        shop_name=shop_name,
        phone=contact,
        country=country,
        street_address1=street_address1,
        street_address2=street_address2,
        city=city,
        state=state,
        zipcode=zipcode,
        location_name=location_name,
        lat=location_lat,
        lng=location_lng,
        business_type=business_type,
        photo=business_logo,
        shop_password=password1,

    )

    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([ ])
def setup_shop_view(request):
    payload = {}
    data = {}
    errors = {}



    shop_id = request.data.get('shop_id', '')
    description = request.data.get('description', '')
    shop_exteriors = request.data.get('shop_exteriors', [])
    shop_interiors = request.data.get('shop_interiors', [])
    shop_works = request.data.get('shop_works', [])
    business_days = request.data.get('business_days', [])
    business_hours_open = request.data.get('business_hours_open', [])
    business_hours_close = request.data.get('business_hours_close', [])
    special_features = request.data.get('special_features', [])


    if not description:
        errors['description'] = ["Description required"]

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    shop = Shop.objects.get(shop_id=shop_id)
    shop.description = description
    shop.business_days = business_days
    shop.business_hours_open = business_hours_open
    shop.business_hours_close = business_hours_close
    shop.special_features = special_features


    shop.save()

    for interior in shop_interiors:
        ShopInterior.objects.create(
            shop=shop,
            photo=interior
        )


    for exterior in shop_exteriors:
        ShopExterior.objects.create(
            shop=shop,
            photo=exterior
        )


    for work in shop_works:
        ShopWork.objects.create(
            shop=shop,
            photo=work
        )


    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([ ])
def setup_services_view(request):
    payload = {}
    data = {}
    errors = {}



    shop_id = request.data.get('shop_id', '')
    services = request.data.get('services', '')

    if not services:
        errors['services'] = ["Services required"]

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    shop = Shop.objects.get(shop_id=shop_id)

    for service in services:
        ShopService.objects.create(
            shop=shop,
            service_type=service['service_type'],
            price=service['price'],
            duration=service['duration'],
            description=service['description'],
        )


    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([ ])
def setup_staff_view(request):
    payload = {}
    data = {}
    errors = {}



    shop_id = request.data.get('shop_id', '')
    staffs = request.data.get('staffs', '')

    if not staffs:
        errors['staffs'] = ["Staffs required"]

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    shop = Shop.objects.get(shop_id=shop_id)

    for staff in staffs:
        ShopStaff.objects.create(
            shop=shop,
            staff_name=staff['staff_name'],
            role=staff['role'],
            photo=staff['photo'],
        )


    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([])
@authentication_classes([ ])
def list_all_shops_view(request):
    payload = {}
    data = {}
    errors = {}



    shop_id = request.data.get('shop_id', '')

    if not shop_id:
        errors['shop_id'] = ["Shop id required"]

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    shops = Shop.objects.all()

    shops_serializer = ShopSerializer(shops, many=True)
    if shops_serializer:
        _shops = shops_serializer.data
        data['shops'] = _shops

    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_shop_view2222(request):
    payload = {}
    data = {}
    errors = {}



    shop_name = request.data.get('shop_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')
    country = request.data.get('country', '')
    street_address1 = request.data.get('street_address1', '')
    street_address2 = request.data.get('street_address2', '')
    city = request.data.get('city', '')
    state = request.data.get('state', '')
    zipcode = request.data.get('zipcode', '')
    location_name = request.data.get('location_name', '')
    location_lat = request.data.get('location_lat', '')
    location_lng = request.data.get('location_lng', '')
    business_type = request.data.get('business_type', '')
    business_logo = request.data.get('business_logo', '')
    password1 = request.data.get('password1', '')
    password2 = request.data.get('password2', '')

    if not shop_name:
        errors['shop_name'] = ["Shop name required"]

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    new_shop = Shop.objects.create(
        email=email,
        phone=contact,
        country=country,
        street_address1=street_address1,
        street_address2=street_address2,
        city=city,
        state=state,
        zipcode=zipcode,
        location_name=location_name,
        location_lat=location_lat,
        location_lng=location_lng,
        business_type=business_type,
        business_logo=business_logo,
        shop_password=password1,

    )

    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)

