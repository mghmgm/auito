# Generated by Django 5.0.6 on 2024-06-06 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_car_image_alter_post_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="car",
            name="image",
        ),
    ]
