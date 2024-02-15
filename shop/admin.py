from django.contrib import admin

from shop.models import Shop, ShopInterior, ShopExterior, ShopWork, ShopService, ShopStaff

# Register your models here.
admin.site.register(Shop)
admin.site.register(ShopInterior)
admin.site.register(ShopExterior)
admin.site.register(ShopWork)
admin.site.register(ShopService)
admin.site.register(ShopStaff)
