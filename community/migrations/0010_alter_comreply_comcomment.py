# Generated by Django 4.2.4 on 2023-09-01 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_remove_comcomment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comreply',
            name='comcomment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comreplies', to='community.comcomment'),
        ),
    ]
