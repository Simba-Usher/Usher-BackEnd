# Generated by Django 4.2.4 on 2023-09-04 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_customuser_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
