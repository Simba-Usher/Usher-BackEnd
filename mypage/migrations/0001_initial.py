# Generated by Django 4.2.4 on 2023-09-03 17:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(max_length=50, unique=True)),
                ('performance_location', models.CharField(max_length=20)),
                ('performance_date', models.DateTimeField()),
                ('reservation_site', models.CharField(max_length=20)),
                ('discount_method', models.CharField(max_length=10)),
                ('price', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
