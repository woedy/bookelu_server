# Generated by Django 5.0.1 on 2024-01-22 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "user_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True)),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("full_name", models.CharField(blank=True, max_length=255, null=True)),
                ("fcm_token", models.TextField(blank=True, null=True)),
                ("email_token", models.CharField(blank=True, max_length=10, null=True)),
                ("email_verified", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_online", models.BooleanField(default=True)),
                ("staff", models.BooleanField(default=False)),
                ("admin", models.BooleanField(default=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
