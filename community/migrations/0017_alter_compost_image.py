# Generated by Django 4.2.5 on 2023-09-14 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0016_alter_comcomment_compost"),
    ]

    operations = [
        migrations.AlterField(
            model_name="compost",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="compost_media/"),
        ),
    ]
