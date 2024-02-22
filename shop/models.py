import os
import random

from django.db import models
from django.db.models.signals import pre_save

from bookelu_project.utils import unique_shop_id_generator


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_shop_logo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_logo/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_shop_interior_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_interior/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )




def upload_shop_exterior_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_exterior/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



def upload_shop_work_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_work/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_staff_photo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_work/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_package_photo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_work/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



BUSINESS_TYPE_CHOICES = (
    ('Private', 'Private'),
    ('Public', 'Public'),

)
class Shop(models.Model):
    shop_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    shop_password = models.CharField(max_length=255, blank=True, null=True)

    business_type = models.CharField(max_length=255, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField( null=True, blank=True)


    business_days = models.CharField(max_length=255, null=True, blank=True)
    business_hours_open = models.CharField(max_length=255, null=True, blank=True)
    business_hours_close = models.CharField(max_length=255, null=True, blank=True)

    special_features = models.CharField(max_length=255, null=True, blank=True)

    rating = models.DecimalField(default=0.0, decimal_places=2, max_digits=2, null=True, blank=True)


    photo = models.ImageField(upload_to=upload_shop_logo_path, null=True, blank=True)

    verify_code = models.CharField(max_length=10, blank=True, null=True)

    open = models.BooleanField(default=True)


    street_address1 = models.CharField(max_length=255, null=True, blank=True)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

def pre_save_shop_id_receiver(sender, instance, *args, **kwargs):
    if not instance.shop_id:
        instance.shop_id = unique_shop_id_generator(instance)

pre_save.connect(pre_save_shop_id_receiver, sender=Shop)



class ShopInterior(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_interior')
    photo = models.ImageField(upload_to=upload_shop_interior_path, null=True, blank=True)



class ShopExterior(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_exterior')
    photo = models.ImageField(upload_to=upload_shop_exterior_path, null=True, blank=True)


class ShopWork(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_work')
    photo = models.ImageField(upload_to=upload_shop_work_path, null=True, blank=True)


SERVICE_CHOICES = (
    ('Haircut', 'Haircut'),
    ('Nail Tech', 'Nail Tech'),
    ('Massage', 'Massage'),
    ('Hairstyle', 'Hairstyle'),


)
class ShopService(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_services')
    service_type = models.CharField(max_length=200, choices=SERVICE_CHOICES,  null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField( null=True, blank=True)





class ShopStaff(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_staffs')
    staff_name = models.CharField(max_length=200,  null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_staff_photo_path, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)


class ServiceSpecialist(models.Model):
    service = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='service_specialist')
    specialist = models.ForeignKey(ShopStaff, on_delete=models.CASCADE, related_name='staff_specialist')


class ShopPackage(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_packages')
    package_name = models.CharField(max_length=200,  null=True, blank=True)
    photo = models.ImageField(upload_to=upload_package_photo_path, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)

