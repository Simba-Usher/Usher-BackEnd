# Generated by Django 4.2.4 on 2023-09-05 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mypage", "0005_memo"),
    ]

    operations = [
        migrations.AddField(
            model_name="memo",
            name="title",
            field=models.CharField(default=0, max_length=20),
        ),
    ]
