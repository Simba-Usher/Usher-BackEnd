# Generated by Django 4.2.4 on 2023-09-07 18:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0014_mainpost_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpost',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_mainposts', to=settings.AUTH_USER_MODEL),
        ),
    ]
