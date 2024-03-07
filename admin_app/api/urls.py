from django.urls import path

from admin_app.api.views import overview_view, list_all_shops_admin_view
from bookings.api.views import shop_bookings_view, shop_booking_detail_view

app_name = 'admin_app'

urlpatterns = [
    path('overview/', overview_view, name="overview_view"),
    path('list-vendors-admin/', list_all_shops_admin_view, name="list_all_shops_admin_view"),
]
