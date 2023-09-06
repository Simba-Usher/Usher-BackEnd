# Generated by Django 4.2.5 on 2023-09-06 15:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("community", "0011_compost_views"),
    ]

    operations = [
        migrations.AddField(
            model_name="compost",
            name="liked_users",
            field=models.ManyToManyField(
                related_name="liked_composts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]