# Generated by Django 5.1 on 2024-08-28 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_photo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car_image",
            name="image",
            field=models.ImageField(max_length=500, upload_to="photo_for_users"),
        ),
    ]
