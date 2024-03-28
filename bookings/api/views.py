from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from bookings.api.serializers import ListBookingSerializer, BookingSerializer
from bookings.models import Booking, BookingPayment, BookingRating, WalkInBooking
from chats.models import PrivateChatRoom
from shop.models import Shop, ShopService, ShopStaff
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_bookings_view(request):
    payload = {}
    data = {}
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

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    bookings = Booking.objects.filter(shop=shop).order_by('-created_at')

    if search_query:
        bookings = bookings.filter(booking_id__icontains=search_query)

    paginator = Paginator(bookings, page_size)

    try:
        paginated_bookings = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_bookings = paginator.page(1)
    except EmptyPage:
        paginated_bookings = paginator.page(paginator.num_pages)

    booking_serializer = ListBookingSerializer(paginated_bookings, many=True)

    data['bookings'] = booking_serializer.data
    data['pagination'] = {
        'page_number': paginated_bookings.number,
        'total_pages': paginator.num_pages,
        'next': paginated_bookings.next_page_number() if paginated_bookings.has_next() else None,
        'previous': paginated_bookings.previous_page_number() if paginated_bookings.has_previous() else None,
    }

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




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def book_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.data.get('user_id', '')
    shop_id = request.data.get('shop_id', '')
    staff_id = request.data.get('staff_id', '')
    service_id = request.data.get('service_id', '')
    date = request.data.get('date', '')
    time = request.data.get('time', '')
    home_service = request.data.get('home_service', '')
    notes = request.data.get('notes', '')

    if not user_id:
        errors['user_id'] = ['User id is required.']

    if not shop_id:
        errors['shop_id'] = ['Shop id is required.']

    if not date:
        errors['date'] = ['Booking date is required.']

    if not staff_id:
        errors['staff_id'] = ['Staff id is required.']

    if not time:
        errors['time'] = ['Booking time is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except:
        errors['shop_id'] = ['Shop does not exist.']

    try:
        staff = ShopStaff.objects.get(staff_id=staff_id)
    except:
        errors['staff_id'] = ['Staff does not exist.']

    try:
        shop_service = ShopService.objects.get(service_id=service_id)
    except:
        errors['service_id'] = ['Service does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    new_booking = Booking.objects.create(
        shop=shop,
        service=shop_service,
        client=user,
        booked_staff=staff,
        home_service=home_service,
        booking_date=date,
        booking_time=time,
        notes=notes,
    )


    #Generate room
    new_room = PrivateChatRoom.objects.create(
       shop=shop.user,
       client=user
   )

    new_booking.room = new_room
    new_booking.save()





    data['booking_id'] = new_booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def walkin_booking_view(request):
    payload = {}
    data = {}
    errors = {}

    shop_id = request.data.get('shop_id', '')
    staff_id = request.data.get('staff_id', '')
    service_id = request.data.get('service_id', '')
    date = request.data.get('date', '')
    time = request.data.get('time', '')
    home_service = request.data.get('home_service', '')
    notes = request.data.get('notes', '')

    customer_name = request.data.get('customer_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')
    country = request.data.get('country', '')
    practitioner = request.data.get('practitioner', '')

    if not shop_id:
        errors['shop_id'] = ['Shop id is required.']

    if not date:
        errors['date'] = ['Booking date is required.']

    if not staff_id:
        errors['staff_id'] = ['Staff id is required.']

    if not time:
        errors['time'] = ['Booking time is required.']

    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except:
        errors['shop_id'] = ['Shop does not exist.']

    try:
        staff = ShopStaff.objects.get(staff_id=staff_id)
    except:
        errors['staff_id'] = ['Staff does not exist.']

    try:
        shop_service = ShopService.objects.get(id=service_id)
    except:
        errors['service_id'] = ['Service does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    new_booking = Booking.objects.create(
        shop=shop,
        service=shop_service,
        booked_staff=staff,
        home_service=home_service,
        booking_date=date,
        booking_time=time,
        notes=notes,
    )



    new_walkin = WalkInBooking.objects.create(
       booking=new_booking,
       customer_name=customer_name,
       contact=contact,
       email=email,
       country=country,
       practitioner=practitioner,
   )





    data['booking_id'] = new_booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def client_bookings_view(request):
    payload = {}
    data = {}
    user_data = {}
    errors = {}

    bookings = []


    user_id = request.query_params.get('user_id', None)

    if not user_id:
        errors['user_id'] = ['User ID is required.']

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)




    _upcoming = Booking.objects.filter(client=user).filter(status="Pending").order_by('-created_at')
    upcoming_serializer = ListBookingSerializer(_upcoming, many=True)
    if upcoming_serializer:
        _upcoming = upcoming_serializer.data

    data['upcoming'] = _upcoming


    _history = Booking.objects.filter(client=user).filter(status="Completed").order_by('-created_at')
    history_serializer = ListBookingSerializer(_history, many=True)
    if history_serializer:
        _history = history_serializer.data

    data['history'] = _history

    _all_bookings = Booking.objects.filter(client=user).order_by('-created_at')
    all_bookings_serializer = ListBookingSerializer(_all_bookings, many=True)
    if all_bookings_serializer:
        _all_bookings = all_bookings_serializer.data

    data['all_bookings'] = _all_bookings




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def reschedule_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')
    date = request.data.get('date', '')
    time = request.data.get('time', '')

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']

    if not date:
        errors['date'] = ['Booking date is required.']

    if not time:
        errors['time'] = ['Booking time is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    booking.booking_date = date
    booking.booking_time = time
    booking.re_scheduled = True
    booking.save()


    data['booking_id'] = booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def cancel_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    booking.status = "Canceled"
    booking.save()


    data['booking_id'] = booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def make_payment_view(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')
    payment_method = request.data.get('payment_method', '')
    amount = request.data.get('amount', '')

    if not payment_method:
        errors['payment_method'] = ['Payment method is required.']

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']

    if not amount:
        errors['amount'] = ['Amount is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    booking.paid = True
    booking.save()

    payment = BookingPayment.objects.create(
        booking=booking,
        payment_method=payment_method,
        amount=amount,
    )

    data['booking_id'] = booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def booking_ratings(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')
    rating = request.data.get('rating', '')
    report = request.data.get('report', '')

    if not rating:
        errors['rating'] = ['Rating is required.']

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']


    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    rating = BookingRating.objects.create(
        booking=booking,
        rating=rating,
        report=report,
    )

    data['booking_id'] = booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def add_split_view(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')
    booking_split_from = request.data.get('booking_split_from', '')
    booking_split_to = request.data.get('booking_split_to', '')

    if not booking_split_from:
        errors['booking_split_from'] = ['Split from is required.']

    if not booking_split_to:
        errors['booking_split_to'] = ['Split to is required.']

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']


    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


    booking.split = True
    booking.booking_split_from = booking_split_from
    booking.booking_split_to = booking_split_to
    booking.save()

    data['booking_id'] = booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

