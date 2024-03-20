# Generated by Django 5.0.2 on 2024-03-13 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_home_service'),
        ('chats', '0003_alter_privatechatroom_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking_chat_rooms', to='chats.privatechatroom'),
        ),
    ]
