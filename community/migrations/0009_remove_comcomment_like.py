# Generated by Django 4.2.4 on 2023-09-01 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_alter_compost_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comcomment',
            name='like',
        ),
    ]
