from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_profile.models import UserProfile

User = get_user_model()


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_user_profile_view(request):
    payload = {}
    data = {}
    user_data = {}

    user_id = request.query_params.get('user_id', None)

    user = User.objects.get(user_id=user_id)
    personal_info = UserProfile.objects.get(user=user)

    user_data['user_id'] = user.user_id
    user_data['email'] = user.email
    user_data['full_name'] = user.full_name

    user_data['photo'] = personal_info.photo.url
    user_data['phone'] = personal_info.phone
    data['user_data'] = user_data

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def update_user_profile_view(request):
    payload = {}
    data = {}
    user_data = {}

    user_id = request.data.get('user_id', '')

    email = request.data.get('email', '0').lower()
    full_name = request.data.get('full_name', '')

    phone = request.data.get('phone', '')
    photo = request.data.get('photo', '')

    user = User.objects.get(user_id=user_id)
    user.email = email
    user.full_name = full_name
    user.save()

    personal_info = UserProfile.objects.get(user=user)
    personal_info.phone = phone
    personal_info.save()

    if photo is not "":
        personal_info.photo = photo
        personal_info.save()


    data['user_id'] = user.user_id
    data['email'] = user.email
    data['full_name'] = user.full_name

    data['phone'] = personal_info.phone
    data['country'] = personal_info.country
    data['photo'] = personal_info.photo.url



    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)