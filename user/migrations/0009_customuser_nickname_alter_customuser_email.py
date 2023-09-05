# Generated by Django 4.2.4 on 2023-09-04 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_customuser_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(default=0, max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
