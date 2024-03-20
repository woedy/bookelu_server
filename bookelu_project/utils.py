import random
import re
import string
from django.contrib.auth import get_user_model, authenticate




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_otp_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def unique_user_id_generator(instance):
    """
    This is for a django project with a user_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    user_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=user_id).exists()
    if qs_exists:
        return
    return user_id





def unique_shop_id_generator(instance):
    """
    This is for a django project with a shop_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    shop_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(shop_id=shop_id).exists()
    if qs_exists:
        return
    return shop_id

def generate_email_token():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code




def unique_service_id_generator(instance):
    """
    This is for a service_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    service_id = "BK-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(S)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(service_id=service_id).exists()
    if qs_exists:
        return None
    return service_id



def unique_booking_id_generator(instance):
    """
    This is for a booking_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    booking_id = "BK-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(AP)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(booking_id=booking_id).exists()
    if qs_exists:
        return None
    return booking_id

def unique_room_id_generator(instance):
    """
    This is for a room_id field
    :param instance:
    :return:
    """
    size = random.randint(30, 45)
    room_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(room_id=room_id).exists()
    if qs_exists:
        return None
    return room_id


def unique_staff_id_generator(instance):
    """
    This is for a staff_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    staff_id = "STF-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(S)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(staff_id=staff_id).exists()
    if qs_exists:
        return None
    return staff_id





