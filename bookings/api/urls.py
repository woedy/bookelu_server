from django.urls import path

from bookings.api.views import shop_bookings_view, shop_booking_detail_view

app_name = 'bookings'

urlpatterns = [
    path('shop-bookings/', shop_bookings_view, name="shop_bookings_view"),
    path('shop-booking-detail/', shop_booking_detail_view, name="shop_booking_detail_view"),
]
