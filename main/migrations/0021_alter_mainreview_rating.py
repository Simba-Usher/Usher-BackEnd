# Generated by Django 4.2.5 on 2023-09-15 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0020_alter_mainpost_liked_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mainreview",
            name="rating",
            field=models.IntegerField(
                choices=[(1, "1점"), (2, "2점"), (3, "3점"), (4, "4점"), (5, "5점")],
                default=0,
            ),
        ),
    ]
