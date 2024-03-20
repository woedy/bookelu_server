import re
from celery import chain

from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.template.loader import get_template
from bookelu_project.tasks import send_generic_email

from accounts.api.serializers import UserRegistrationSerializer
from activities.models import AllActivity
from bookelu_project import settings
from bookelu_project.utils import generate_email_token
from payments.models import PaymentSetup
from shop.api.serializers import ShopDetailSerializer, ListShopsSerializer, ShopStaffSerializer
from shop.models import Shop, ShopInterior, ShopExterior, ShopWork, ShopService, ShopStaff, ShopPackage
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage, send_mail

User = get_user_model()

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def check_shop_email_exists(request):
    payload = {}
    data = {}
    errors = {}

    email = request.data.get('email', '')


    if not email:
        errors['email'] = ['User Email is required.']
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def admin_add_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    full_name = request.data.get('full_name', '')
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
    password = request.data.get('password', 'Bookelu123!_')
    password2 = request.data.get('password2', 'Bookelu123!_')

    if not email:
        errors['email'] = ['User Email is required.']
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']

    if not full_name:
        errors['full_name'] = ['Shop full name is required.']

    if not contact:
        errors['contact'] = ['Contact number is required.']

    if not password:
        errors['password'] = ['Password is required.']

    if not password2:
        errors['password2'] = ['Password2 is required.']

    if password != password2:
        errors['password'] = ['Passwords dont match.']

    if not is_valid_password(password):
        errors['password'] = [
            'Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data["user_id"] = user.user_id
        data["email"] = user.email
        data["shop_name"] = user.full_name

        user.user_type = "Shop"
        user.save()

    new_shop = Shop.objects.create(
        user=user,
        email=email,
        shop_name=full_name,
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

    )

    new_shop.shop_registered = True
    new_shop.save()

    token = Token.objects.get(user=user).key
    data['token'] = token

    data['shop_id'] = new_shop.shop_id

    email_token = generate_email_token()

    user = User.objects.get(email=email)
    user.email_token = email_token
    user.save()

    context = {
        'email_token': email_token,
        'email': user.email,
        'full_name': user.full_name
    }

    txt_ = get_template("registration/emails/verify.html").render(context)
    html_ = get_template("registration/emails/verify.txt").render(context)

    subject = 'EMAIL CONFIRMATION CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    #  # Use Celery chain to execute tasks in sequence
    #  email_chain = chain(
    #      send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    #  )
    #  # Execute the Celery chain asynchronously
    #  email_chain.apply_async()

    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )


    #
    new_activity = AllActivity.objects.create(
        user=user,
        subject="Shop Registration",
        body= "Admin Just created an account."
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


# Create your views here.
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def add_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    full_name = request.data.get('full_name', '')
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
    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    if not email:
        errors['email'] = ['User Email is required.']
    elif not is_valid_email(email):
        errors['email'] = ['Valid email required.']
    elif check_email_exist(email):
        errors['email'] = ['Email already exists in our database.']

    if not full_name:
        errors['full_name'] = ['Shop full name is required.']

    if not contact:
        errors['contact'] = ['Contact number is required.']

    if not password:
        errors['password'] = ['Password is required.']

    if not password2:
        errors['password2'] = ['Password2 is required.']

    if password != password2:
        errors['password'] = ['Passwords dont match.']

    if not is_valid_password(password):
        errors['password'] = [
            'Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data["user_id"] = user.user_id
        data["email"] = user.email
        data["shop_name"] = user.full_name

        user.user_type = "Shop"
        user.save()

    new_shop = Shop.objects.create(
        user=user,
        email=email,
        shop_name=full_name,
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

    )

    new_shop.shop_registered = True
    new_shop.save()

    token = Token.objects.get(user=user).key
    data['token'] = token

    data['shop_id'] = new_shop.shop_id

    email_token = generate_email_token()

    user = User.objects.get(email=email)
    user.email_token = email_token
    user.save()

    context = {
        'email_token': email_token,
        'email': user.email,
        'full_name': user.full_name
    }

    txt_ = get_template("registration/emails/verify.html").render(context)
    html_ = get_template("registration/emails/verify.txt").render(context)

    subject = 'EMAIL CONFIRMATION CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Use Celery chain to execute tasks in sequence
    # email_chain = chain(
    #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    # )
    # # Execute the Celery chain asynchronously
    # email_chain.apply_async()

    send_mail(
        subject,
        txt_,
        from_email,
        recipient_list,
        html_message=html_,
        fail_silently=False,
    )



    #
    new_activity = AllActivity.objects.create(
        user=user,
        subject="Shop Registration",
        body=user.email + " Just created an account."
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    description = request.data.get('description', '')
    business_days = request.data.get('business_days', '')
    business_hours_open = request.data.get('business_hours_open', '')
    business_hours_close = request.data.get('business_hours_close', '')
    special_features = request.data.get('special_features', '')

    if not description:
        errors['description'] = ["Description required"]

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

    shop = Shop.objects.get(shop_id=shop_id)
    shop.description = description
    shop.business_days = business_days
    shop.business_hours_open = business_hours_open
    shop.business_hours_close = business_hours_close
    shop.special_features = special_features

    shop.save()


    shop.shop_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_exterior_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    shop_exterior = request.data.get('shop_exterior', "")

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

    shop = Shop.objects.get(shop_id=shop_id)
    shop.save()


    ShopExterior.objects.create(
            shop=shop,
            photo=shop_exterior
        )

    shop.shop_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_interior_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    shop_interior = request.data.get('shop_interior', "")

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

    shop = Shop.objects.get(shop_id=shop_id)
    shop.save()


    ShopInterior.objects.create(
            shop=shop,
            photo=shop_interior
        )

    shop.shop_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_work_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    shop_work = request.data.get('shop_work', "")

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

    shop = Shop.objects.get(shop_id=shop_id)
    shop.save()


    ShopWork.objects.create(
            shop=shop,
            photo=shop_work
        )

    shop.shop_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_shop_view222(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    description = request.data.get('description', '')
    shop_exteriors = request.data.get('shop_exteriors', [])
    shop_interiors = request.data.get('shop_interiors', [])
    shop_works = request.data.get('shop_works', [])
    business_days = request.data.get('business_days', '')
    business_hours_open = request.data.get('business_hours_open', '')
    business_hours_close = request.data.get('business_hours_close', '')
    special_features = request.data.get('special_features', '')

    if not description:
        errors['description'] = ["Description required"]

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

    shop.shop_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_services_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    service_type = request.data.get('service_type', '')
    price = request.data.get('price', '')
    duration = request.data.get('duration', '')
    description = request.data.get('description', '')

    if not service_type:
        errors['service_type'] = ["Services type required"]

    if not price:
        errors['price'] = ["Price required"]

    if not description:
        errors['description'] = ["Description required"]

    if not duration:
        errors['duration'] = ["Duration required"]

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

    shop = Shop.objects.get(shop_id=shop_id)

    ShopService.objects.create(
            shop=shop,
            service_type=service_type,
            price=price,
            duration=duration,
            description=description,
        )

    shop.service_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_services_view22(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    services = request.data.get('services', '')

    if not services:
        errors['services'] = ["Services required"]

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

    shop = Shop.objects.get(shop_id=shop_id)

    for service in services:
        ShopService.objects.create(
            shop=shop,
            service_type=service['service_type'],
            price=service['price'],
            duration=service['duration'],
            description=service['description'],
        )

    shop.service_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_staff_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    staff_name = request.data.get('staff_name', '')
    role = request.data.get('role', '')
    photo = request.data.get('photo', '')

    if not role:
        errors['role'] = ["Role name required"]

    if not staff_name:
        errors['staff_name'] = ["Staff name required"]

    if not photo:
        errors['photo'] = ["Photo required"]

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

    shop = Shop.objects.get(shop_id=shop_id)

    ShopStaff.objects.create(
            shop=shop,
            staff_name=staff_name,
            role=role,
            photo=photo,
        )

    shop.staff_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_staff_view222222(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    staffs = request.data.get('staffs', '')

    if not staffs:
        errors['staffs'] = ["Staffs required"]

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

    shop = Shop.objects.get(shop_id=shop_id)

    for staff in staffs:
        ShopStaff.objects.create(
            shop=shop,
            staff_name=staff['staff_name'],
            role=staff['role'],
            photo=staff['photo'],
        )

    shop.staff_setup = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def setup_payment_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    platform = request.data.get('platform', '')
    public_api_key = request.data.get('public_api_key', '')

    if not platform:
        errors['platform'] = ["Platform required"]

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

    shop = Shop.objects.get(shop_id=shop_id)

    new_payment_setup = PaymentSetup.objects.create(
        shop=shop,
        platform=platform,
        public_api_key=public_api_key
    )

    shop.payment_setup = True
    shop.registration_complete = True
    shop.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def remove_staff_view(request):
    payload = {}
    data = {}
    errors = {}

    staff_id = request.data.get('staff_id', '')

    if not staff_id:
        errors['staff_id'] = ['Staff ID is required.']

    try:
        staff = ShopStaff.objects.get(staff_id=staff_id)
    except:
        errors['staff_id'] = ['Staff does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    staff.delete()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_package_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    package_name = request.data.get('package_name', '')
    price = request.data.get('price', '')
    photo = request.data.get('photo', '')

    if not package_name:
        errors['package_name'] = ["Package Name required."]

    if not price:
        errors['price'] = ["Price required."]

    if not photo:
        errors['photo'] = ["Photo required."]

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

    shop = Shop.objects.get(shop_id=shop_id)

    ShopPackage.objects.create(
            shop=shop,
            package_name=package_name,
            price=price,
            photo=photo,

        )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_package_view22(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    packages = request.data.get('packages', '')

    if not packages:
        errors['packages'] = ["Add at least one package required"]

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

    shop = Shop.objects.get(shop_id=shop_id)

    for package in packages:
        ShopPackage.objects.create(
            shop=shop,
            package_name=package['package_name'],
            price=package['price'],
            photo=package['photo'],

        )

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def list_all_shops_view(request):
    payload = {}
    data = {}
    errors = {}

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    shops = Shop.objects.all().filter(registration_complete=True)

    shops_serializer = ListShopsSerializer(shops, many=True)
    if shops_serializer:
        _shops = shops_serializer.data
        data['shops'] = _shops

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_details_view(request):
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


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_staffs_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

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

    _staffs = ShopStaff.objects.filter(shop=shop).order_by('-created_at')
    staffs_serializer = ShopStaffSerializer(_staffs, many=True)
    if staffs_serializer:
        staffs = staffs_serializer.data

    payload['message'] = "Successful"
    payload['data'] = staffs

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_shop_view(request):

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
            body=shop.user.email + " Just deleted their shop. " + shop.shop_name
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





def check_email_exist(email):
    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    else:
        return False


def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    # Check for at least 8 characters
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        return False

    # Check for at least one special character
    if not re.search(r'[-!@#\$%^&*_()-+=/.,<>?"~`£{}|:;]', password):
        return False

    return True
