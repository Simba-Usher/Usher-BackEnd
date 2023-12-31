# Generated by Django 4.2.5 on 2023-09-08 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mypage", "0008_rename_user_ticket_writer"),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketMemo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("content", models.TextField(max_length=100)),
                (
                    "ticket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_memo",
                        to="mypage.ticket",
                    ),
                ),
            ],
        ),
    ]
