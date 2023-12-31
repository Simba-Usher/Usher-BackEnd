# Generated by Django 4.2.5 on 2023-09-15 04:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0019_alter_mainpost_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainpost",
            name="liked_users",
            field=models.ManyToManyField(
                blank=True, related_name="liked_mainposts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
