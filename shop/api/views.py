from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response


# Create your views here.
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def add_shop_view(request):
    payload = {}
    data = {}
    errors = {}



    shop_name = request.data.get('shop_name', '')

    if not shop_name:
        errors['shop_name'] = ["Shop name required"]



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    payload['message'] = "Successful"
    payload['data'] = data


    return Response(payload, status=status.HTTP_200_OK)

