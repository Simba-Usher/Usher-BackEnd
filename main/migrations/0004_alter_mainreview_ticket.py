# Generated by Django 4.2.4 on 2023-09-03 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0001_initial'),
        ('main', '0003_mainpost_image_mainreview_ticket_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainreview',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mainreviews', to='mypage.ticket'),
        ),
    ]