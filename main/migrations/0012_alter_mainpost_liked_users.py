# Generated by Django 4.2.5 on 2023-09-06 16:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0011_remove_mainreview_liked_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainpost",
            name="liked_users",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="liked_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
