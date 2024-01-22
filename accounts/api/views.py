import re

from celery import chain
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from accounts.api.serializers import UserRegistrationSerializer
from activities.models import AllActivity
from bookelu_project.utils import generate_email_token
from bookelu_project.tasks import send_registration_email
from user_profile.models import UserProfile

User = get_user_model()


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def register_user(request):

    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()
        full_name = request.data.get('full_name', "")
        phone = request.data.get('phone', "")
        country = request.data.get('country', "")
        password = request.data.get('password', "")
        password2 = request.data.get('password2', "")


        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email already exists in our database.']

        if not full_name:
            errors['full_name'] = ['Full Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not country:
            errors['country'] = ['Country is required.']


        if not password:
            errors['password'] = ['Password is required.']

        if not password2:
            errors['password2'] = ['Password2 is required.']

        if password != password2:
            errors['password'] = ['Passwords dont match.']

        if not is_valid_password(password):
            errors['password'] = ['Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data["user_id"] = user.user_id
            data["email"] = user.email
            data["full_name"] = user.full_name

            user_profile = UserProfile.objects.create(
                user=user,
                phone=phone,
                country=country

            )
            user_profile.save()

            data['phone'] = user_profile.phone
            data['country'] = user_profile.country

        token = Token.objects.get(user=user).key
        data['token'] = token

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
        email_chain = chain(
            send_registration_email.si(subject, txt_, from_email, recipient_list, html_),
        )
        # Execute the Celery chain asynchronously
        email_chain.apply_async()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Registration",
            body=user.email + " Just created an account."
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
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True

