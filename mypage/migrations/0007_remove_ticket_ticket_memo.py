# Generated by Django 4.2.4 on 2023-09-06 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0006_memo_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_memo',
        ),
    ]
