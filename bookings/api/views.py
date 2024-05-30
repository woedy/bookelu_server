import re
from decimal import Decimal

from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from activities.models import AllActivity
from bank_account.models import BankAccount
from bookings.api.serializers import ListBookingSerializer, BookingSerializer
from bookings.models import Booking, BookingPayment, BookingRating, WalkInBooking
from chats.api.serializers import PrivateRoomChatMessageSerializer, PrivateRoomSerializer
from chats.api.views import send_message
from chats.models import PrivateChatRoom, PrivateRoomChatMessage
from shop.models import Shop, ShopService, ShopStaff, ShopPackage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from slots.models import StaffSlot, TimeSlot
from django.db.models import Q

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
def book_appointment_view1111111(request):
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
@permission_classes([])
@authentication_classes([])
def book_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', '')
        shop_id = request.data.get('shop_id', '')
        staff_id = request.data.get('staff_id', '')
        service_id = request.data.get('service_id', '')
        package_id = request.data.get('package_id', '')
        home_service = request.data.get('home_service', '')
        notes = request.data.get('notes', '')

        slot_id = request.data.get('slot_id', "")
        slot_time = request.data.get('slot_time', "")

        if not user_id:
            errors['user_id'] = ['Client User ID is required.']

        if not staff_id:
            errors['staff_id'] = ['Staff ID is required.']

        if not service_id:
            errors['service_id'] = ['Service ID is required.']

        if not package_id:
            errors['package_id'] = ['Package ID is required.']

        if not shop_id:
            errors['shop_id'] = ['Shop ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot id is required.']

        if not slot_time:
            errors['slot_time'] = ['Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(slot_time) < 8:
                slot_time += ':00'
        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            errors['shop_id'] = ['Shop does not exist.']

        try:
            client = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            errors['client_id'] = ['Client does not exist']

        try:
            staff = ShopStaff.objects.get(staff_id=staff_id)
        except:
            errors['staff_id'] = ['Staff does not exist']

        try:
            shop_service = ShopService.objects.get(service_id=service_id)
        except:
            errors['service_id'] = ['Service does not exist']

        try:
            package = ShopPackage.objects.get(id=package_id)
        except:
            errors['package_id'] = ['Package does not exist']

        try:
            client_account = BankAccount.objects.get(user=client)
        except BankAccount.DoesNotExist:
            errors['account_id'] = ['Client Bank Account does not exist']

        client_account_balance = client_account.balance

        if extract_amount(package.price) >= client_account_balance:
            errors['booking_id'] = [
                'You dont have enough money to book this appointment. Deposit enough money in your account and book again']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        try:
            staff_slot = StaffSlot.objects.get(id=slot_id)

            #admin = User.objects.filter(company=company, user_type="Admin").first()

            # Check if there's already an appointment for the same date and time

            existing_booking = Booking.objects.filter(
                slot=staff_slot,
                booking_time=slot_time,
                client=client,
                booked_staff=staff
            ).first()



            # Check for appointment interval
            _slot_date = staff_slot.slot_date
            staff_interval = staff.user.availability_interval



            if existing_booking:
                errors['slot_date'] = ['Booking for this date and time already exists.']
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)



            package = ShopPackage.objects.get(id=package_id)


            new_booking = Booking.objects.create(
                shop=shop,
                service=shop_service,
                client=client,
                booked_staff=staff,
                package=package,
                slot=staff_slot,
                home_service=home_service,
                booking_date=staff_slot.slot_date,
                booking_time=slot_time,
                amount_to_pay=package.price,
                notes=notes,
            )

            staff_slot.state = "Partial"
            staff_slot.save()



            # Generate room
            new_room = PrivateChatRoom.objects.create(
                room_id=new_booking.booking_id,
                shop=shop.user,
                client=client
            )

            new_booking.room = new_room
            new_booking.save()

            ### MAKE PAYMENT FOR RESERVATION

            try:
                bookelu_admin = User.objects.get(user_type="Admin")
            except User.DoesNotExist:
                errors['admin'] = ['Admin does not exist']


            try:
                bookelu_account = BankAccount.objects.get(user=bookelu_admin)
            except BankAccount.DoesNotExist:
                return Response({'message': 'Bookelu Bank account not found'}, status=status.HTTP_404_NOT_FOUND)

            if client_account.withdraw(extract_amount(package.price), f'Transfer to {bookelu_account}'):
                bookelu_account.deposit(extract_amount(package.price), f'Transfer from {client_account.account_id}')


                ################################


            slot_times = TimeSlot.objects.filter(staff_slot=staff_slot)

            for time in slot_times:
                if str(time.time) == str(slot_time):
                    print("################")
                    print("The time is in the database")
                    if time.occupied:
                        errors['slot_time'] = ['Slot time is already occupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                    elif not time.occupied:
                        time.occupied = True
                        time.occupant = client
                        time.booking_id = new_booking.id
                        time.save()

            occupied_count = TimeSlot.objects.filter(staff_slot=staff_slot, occupied=True)

            if len(occupied_count) == staff_slot.time_slot_count:
                staff_slot.state = "Occupied"
                staff_slot.save()

            # SEND CLIENT EMAIL
            # client_subject = f"Yay! Your Appointment with {staff.user.full_name} is Confirmed 🎉"
            # client_content = f"Hey {client.full_name},\nGuess what? Your appointment with {staff.user.full_name} on {new_booking.booking_date} at {new_booking.booking_time} is all set! 🌟\n\nMark your calendar and set your reminders because we can't wait to see you!\n\nCheers,\n\nThe {shop.shop_name} Team"
#
            # # SEND PRACTITIONER EMAIL
            # pract_subject = f"New Appointment Alert!🚨"
            # pract_content = f"Hello {staff.user.full_name},\n\nGreat news! {client.full_name} has booked an appointment with you on {new_booking.booking_date} at {new_booking.booking_time}. Time to show off your skills!🌟\n\nBest,\n\nThe {shop.shop_name} Team"
#
            # # Use Celery chain to execute tasks in sequence
            # email_chain = chain(
            #     send_client_email.si(client_subject, client_content, client.email),
            #     send_practitioner_email.si(pract_subject, pract_content, practitioner.email),
            # )
#
            # # Execute the Celery chain asynchronously
            # email_chain.apply_async()
#

            # Add new ACTIVITY
            # new_activity = AllActivity.objects.create(
            #     user=new_appointment.app_admin,
            #     subject="New Appointment Set",
            #     body=f"New appointment set between {staff.user.full_name} and {client.full_name} on {new_booking.booking_date} at {new_booking.booking_time}"
            # )
            # new_activity.save()

            data['booking_id'] = new_booking.booking_id
            payload['data'] = data

        except StaffSlot.DoesNotExist:
            errors['slot_id'] = ['Slot does not exist']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment added successfully"
        return Response(payload)


def extract_amount(value):
    # This regular expression matches digits in the string
    match = re.search(r'\d+', value)
    if match:
        return int(match.group())
    return None
def extract_bookelu_amount(value):
    # This regular expression matches digits in the string
    match = re.search(r'\d+', value)
    if match:
        return int(match.group())
    return None

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
    package_id = request.data.get('package_id', '')
    date = request.data.get('date', '')
    time = request.data.get('time', '')
    notes = request.data.get('notes', '')

    customer_name = request.data.get('customer_name', '')
    contact = request.data.get('contact', '')
    email = request.data.get('email', '')

    if not shop_id:
        errors['shop_id'] = ['Shop id is required.']

    if not date:
        errors['date'] = ['Booking date is required.']

    if not staff_id:
        errors['staff_id'] = ['Staff id is required.']

    if not service_id:
        errors['service_id'] = ['Service id is required.']

    if not package_id:
        errors['package_id'] = ['Package id is required.']

    if not date:
        errors['date'] = ['Booking date is required.']

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
        shop_service = ShopService.objects.get(service_id=service_id)
    except:
        errors['service_id'] = ['Service does not exist.']

    try:
        service_package = ShopPackage.objects.get(id=package_id)
    except:
        errors['package_id'] = ['Package does not exist.']


    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    new_booking = Booking.objects.create(
        shop=shop,
        service=shop_service,
        package=service_package,
        booked_staff=staff,
        booking_date=date,
        booking_time=time,
        notes=notes,
    )



    new_walkin = WalkInBooking.objects.create(
       booking=new_booking,
       customer_name=customer_name,
       contact=contact,
       email=email
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
def reschedule_appointment_view1111(request):
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
@permission_classes([])
@authentication_classes([])
def reschedule_appointment_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', '')
        slot_id = request.data.get('slot_id', '')
        slot_time = request.data.get('slot_time', '')
        #old_slot_time = request.data.get('old_slot_time', '')

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not slot_time:
            errors['slot_time'] = ['Slot time is required.']
        #if not old_slot_time:
        #    errors['old_slot_time'] = ['Old Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(slot_time) < 8:
                slot_time += ':00'

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            errors['booking_id'] = ['Booking does not exist.']

        try:
            staff_slot = StaffSlot.objects.get(id=slot_id)
        except StaffSlot.DoesNotExist:
            errors['slot_id'] = ['Slot does not exist.']

        if not errors:
            # Check if the new slot is available
            existing_booking = Booking.objects.filter(
                slot=staff_slot,
                booking_time=slot_time
            ).exclude(booking_id=booking_id).first()

            if existing_booking:
                errors['slot_time'] = ['Booking for this date and time already exists.']
            else:
                # Update the booking details
                booking.slot = staff_slot
                booking.booking_time = slot_time
                booking.booking_rescheduled_at = timezone.now()
                booking.re_scheduled = True
                booking.save()

                slot_times = TimeSlot.objects.filter(staff_slot=staff_slot)

                for time in slot_times:
                    if str(time.time) == str(slot_time):
                        print("################")
                        print("The time is in the database")
                        if time.occupied:
                            errors['slot_time'] = ['Slot time is already occupied.']
                            payload['message'] = "Errors"
                            payload['errors'] = errors
                            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                        elif not time.occupied:
                            time.occupied = True
                            time.occupant = booking.client
                            time.booking_id = booking.id
                            time.save()
                            #if str(time.time) == str(old_slot_time):
                            #    time.occupied = False
                            #    time.occupant = None
                            #    time.booking_id = None
                            #    time.save()
#
                data['booking_id'] = booking.booking_id
                data['slot_id'] = staff_slot.id
                data['slot_time'] = slot_time

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Appointment rescheduled successfully"
        payload['data'] = data

        return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def reschedule_appointment_view777(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        booking_id = request.data.get('booking_id', "")
        slot_id = request.data.get('slot_id', "")
        old_slot_time = request.data.get('old_slot_time', "")
        new_slot_time = request.data.get('new_slot_time', "")

        if not client_id:
            errors['client_id'] = ['Client User ID is required.']


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not old_slot_time:
            errors['old_slot_time'] = ['Old slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(old_slot_time) < 8:
                old_slot_time += ':00'

        if not new_slot_time:
            errors['new_slot_time'] = ['New slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(new_slot_time) < 8:
                new_slot_time += ':00'


        try:
            client = User.objects.get(user_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist']

        try:
            staff_slot = StaffSlot.objects.get(id=slot_id)
        except StaffSlot.DoesNotExist:
            errors['slot_id'] = ['Slot does not exist']
        except Exception as e:
            errors['slot_id'] = [f'Error fetching slot: {str(e)}']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist']

        slot_times = TimeSlot.objects.all().filter(staff_slot=staff_slot)

        booking.booking_time = new_slot_time
        booking.save()

        for time in slot_times:
            if str(time.time) == str(old_slot_time):
                time.appointment = None
                time.occupied = False
                time.occupant = None
                time.save()

            if str(time.time) == str(new_slot_time):
                time.appointment = booking
                time.occupied = True
                time.occupant = client
                time.save()

        booking.status = "Pending"
        booking.re_scheduled = True
        booking.booking_rescheduled_at = timezone.now()
        booking.save()

        # client_subject = f"Appointment Rescheduled! New Time, Same Great Service 🕐"
        # client_content = f"Hey {booking.client.full_name},\n\nour appointment with {booking.booked_staff.full_name} has been rescheduled to {booking.booking_date} at {booking.booking_time}. We're still super excited to see you!\n\nCheers,\n\nThe {shop.shop_name} Team"
#
        # pact_subject = f"Appointment Rescheduled!🕐"
        # pract_content = f"We want to inform you that the appointment for {appointment.appointee.full_name} has been rescheduled to {appointment.appointment_date} at {appointment.appointment_time}. Please make note of this change in your schedule.\n\nCheers,\n\nThe {company.company_name} Team"
#
        # email_chain = chain(
        #     send_client_email.si(client_subject, client_content, client.email),
        #     send_practitioner_email.si(pact_subject, pract_content, appointment.appointer.email),
        # )
#
        # email_chain.apply_async()
#
        # new_activity = AllActivity.objects.create(
        #     user=appointment.app_admin,
        #     subject="Appointment Rescheduled!",
        #     body=f"Appointment between {appointment.appointer.full_name} and {appointment.appointee.full_name} on {appointment.appointment_date} at {appointment.appointment_time} has been rescheduled."
        # )
        # new_activity.save()

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Booking rescheduled successfully"
        payload['data'] = data

        return Response(payload)




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


    ### MAKE PAYMENT TO SHOP

    try:
        bookelu_admin = User.objects.get(user_type="Admin")
    except User.DoesNotExist:
        errors['admin'] = ['Admin does not exist']

    try:
        client_account = BankAccount.objects.get(user=booking.client)
    except BankAccount.DoesNotExist:
        return Response({'message': 'Client Bank account not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        bookelu_account = BankAccount.objects.get(user=bookelu_admin)
    except BankAccount.DoesNotExist:
        return Response({'message': 'Bookelu Bank account not found'}, status=status.HTTP_404_NOT_FOUND)

    cancellation_policy = Decimal('0.1')
    policy_amount = extract_amount(booking.amount_to_pay) * cancellation_policy
    transfer_amount = extract_amount(booking.amount_to_pay) - policy_amount

    if bookelu_account.withdraw(transfer_amount, f'Transfer to {client_account}'):
        client_account.deposit(transfer_amount, f'Transfer from {bookelu_account.account_id}')
        ################################



    data['booking_id'] = booking.booking_id

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def complete_appointment_view(request):
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


    booking.status = "Completed"
    booking.save()

    ### MAKE PAYMENT TO SHOP

    try:
        bookelu_admin = User.objects.get(user_type="Admin")
    except User.DoesNotExist:
        errors['admin'] = ['Admin does not exist']

    try:
        shop_account = BankAccount.objects.get(user=booking.shop.user)
    except BankAccount.DoesNotExist:
        return Response({'message': 'Shop Bank account not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        bookelu_account = BankAccount.objects.get(user=bookelu_admin)
    except BankAccount.DoesNotExist:
        return Response({'message': 'Bookelu Bank account not found'}, status=status.HTTP_404_NOT_FOUND)

    bookelu_share = Decimal('0.2')
    share_amount = extract_amount(booking.amount_to_pay) * bookelu_share
    transfer_amount = extract_amount(booking.amount_to_pay) - share_amount

    if bookelu_account.withdraw(transfer_amount, f'Transfer to {shop_account}'):
        shop_account.deposit(transfer_amount, f'Transfer from {bookelu_account.account_id}')
        ################################

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



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def send_booking_chat_message(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')
    user_id = request.data.get('user_id', '')
    message = request.data.get('message', '')

    if not user_id:
        errors['user_id'] = ['User ID is required.']

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']


    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    try:
        room_obj = PrivateChatRoom.objects.get(room_id=booking_id)

        message = PrivateRoomChatMessage.objects.create(
            user=user,
            room=room_obj,
            message=message
        )
        message.save()

        # Fetch the messages for the room
        qs = PrivateRoomChatMessage.objects.by_room(room_obj).order_by('-timestamp')[:20]
        serializers = PrivateRoomChatMessageSerializer(qs, many=True)
        if serializers:
            data = serializers.data
            #data['messages'] = data

    except PrivateChatRoom.DoesNotExist:
        errors['booking_id'] = ['Chat room does not exist.']


    # Trigger the event
    send_message(
        booking_id,
        'send-message',
        {'messages': data}
    )
    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def get_booking_chat_messages(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.data.get('booking_id', '')
    user_id = request.data.get('user_id', '')
    message = request.data.get('message', '')

    if not user_id:
        errors['user_id'] = ['User ID is required.']

    if not booking_id:
        errors['booking_id'] = ['Booking id is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']


    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']



    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    try:
        room_obj = PrivateChatRoom.objects.get(room_id=booking_id)

        qs = PrivateRoomChatMessage.objects.by_room(room_obj).order_by('-timestamp')[:20]
        serializers = PrivateRoomChatMessageSerializer(qs, many=True)
        if serializers:
            data = serializers.data
    except PrivateRoomChatMessage.DoesNotExist:
        errors['booking_id'] = ['Chat room messages does not exist.']


    # Trigger the event
    send_message(
        booking_id,
        'get-all-messages',
        {'messages': data}
    )
    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def client_bookings_chat(request):
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
    except:
        errors['user_id'] = ['User does not exist']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)




    client_chat_rooms = PrivateChatRoom.objects.filter(client=user)
    client_chat_rooms_serializers = PrivateRoomSerializer(client_chat_rooms, many=True)
    _client_chat_rooms_serializers = client_chat_rooms_serializers.data

    payload['message'] = "Successful"
    payload['data'] = _client_chat_rooms_serializers

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
def shop_bookings_chat(request):
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
    except:
        errors['user_id'] = ['User does not exist']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)




    shop_chat_rooms = PrivateChatRoom.objects.filter(shop=user)
    shop_chat_rooms_serializers = PrivateRoomSerializer(shop_chat_rooms, many=True)
    _shop_chat_rooms_serializers = shop_chat_rooms_serializers.data

    payload['message'] = "Successful"
    payload['data'] = _shop_chat_rooms_serializers

    return Response(payload, status=status.HTTP_200_OK)