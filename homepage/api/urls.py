from django.urls import path

from homepage.api.views import shop_homepage_view

app_name = 'homepage'

urlpatterns = [
    path('shop-homepage/', shop_homepage_view, name="shop_homepage"),
]
