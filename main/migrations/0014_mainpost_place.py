# Generated by Django 4.2.4 on 2023-09-06 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_mainpost_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpost',
            name='place',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
