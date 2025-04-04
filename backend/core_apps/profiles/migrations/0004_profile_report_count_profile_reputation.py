# Generated by Django 5.0.2 on 2025-03-29 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_alter_profile_city_alter_profile_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="report_count",
            field=models.IntegerField(default=0, verbose_name="Report Count"),
        ),
        migrations.AddField(
            model_name="profile",
            name="reputation",
            field=models.IntegerField(default=100, verbose_name="Reputation"),
        ),
    ]
