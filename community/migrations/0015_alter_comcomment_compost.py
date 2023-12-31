# Generated by Django 4.2.5 on 2023-09-10 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0014_alter_compost_liked_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comcomment",
            name="compost",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comcomments",
                to="community.compost",
            ),
        ),
    ]
