from django.shortcuts import render
from django.urls import path

from shop.api.views import add_shop_view, setup_shop_view, setup_services_view, setup_staff_view, list_all_shops_view

app_name = 'shop'

urlpatterns = [
    path('add-shop/', add_shop_view, name="add_shop_view"),
    path('setup-shop/', setup_shop_view, name="setup_shop_view"),
    path('setup-services/', setup_services_view, name="setup_services_view"),
    path('setup-staffs/', setup_staff_view, name="setup_staff_view"),
    path('list-shops/', list_all_shops_view, name="list_all_shops_view"),


]