# Generated by Django 4.2.4 on 2023-09-01 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='name',
        ),
    ]
