from django.shortcuts import render
from django.urls import path

from shop.api.views import add_shop_view

app_name = 'shop'

urlpatterns = [
    path('add-shop/', add_shop_view, name="add_shop_view"),

]