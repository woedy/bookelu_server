from django.shortcuts import render
from django.urls import path

from shop.api.views import add_shop_view, setup_shop_view, setup_services_view, setup_staff_view, list_all_shops_view, \
    shop_details_view, add_package_view, setup_payment_view, get_staffs_view, remove_staff_view, admin_add_shop_view, \
    check_shop_email_exists, setup_shop_exterior_view, setup_shop_interior_view, setup_shop_work_view, \
    get_services_view, remove_service_view, get_package_view, staff_details_view, package_details_view, \
    remove_package_view, setup_services_staff_view, set_shop_availability, list_shop_availability

app_name = 'shop'

urlpatterns = [
    path('check-shop-email-exists/', check_shop_email_exists, name="check_shop_email_exists"),
    path('admin-add-shop/', admin_add_shop_view, name="admin_add_shop_view"),

    path('add-shop/', add_shop_view, name="add_shop_view"),

    path('setup-shop/', setup_shop_view, name="setup_shop_view"),
    path('setup-shop-exterior/', setup_shop_exterior_view, name="setup_shop_exterior_view"),
    path('setup-shop-interior/', setup_shop_interior_view, name="setup_shop_interior_view"),
    path('setup-shop-work/', setup_shop_work_view, name="setup_shop_work_view"),

    path('setup-services/', setup_services_view, name="setup_services_view"),
    path('setup-services-staff/', setup_services_staff_view, name="setup_services_staff_view"),

    path('setup-payment/', setup_payment_view, name="setup_payment_view"),
    path('add-package/', add_package_view, name="add_package_view"),

    path('setup-staffs/', setup_staff_view, name="setup_staff_view"),

    path('remove-staff/', remove_staff_view, name="remove_staff_view"),
    path('list-shops/', list_all_shops_view, name="list_all_shops_view"),
    path('shop-details/', shop_details_view, name="shop_details_view"),

    path('get-staffs/', get_staffs_view, name="get_staffs_view"),
    path('get-staff-details/', staff_details_view, name="staff_details_view"),

    path('get-services/', get_services_view, name="get_services_view"),

    path('get-packages/', get_package_view, name="get_package_view"),
    path('get-package-details/', package_details_view, name="package_details_view"),
    path('remove-package/', remove_package_view, name="remove_package_view"),

    path('remove-service/', remove_service_view, name="remove_service_view"),

    path('set-shop-availability/', set_shop_availability, name="set_shop_availability"),
    path('list-shop-availability/', list_shop_availability, name="list_shop_availability"),

]