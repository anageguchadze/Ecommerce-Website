# Generated by Django 5.1.5 on 2025-01-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0004_remove_address_is_primary_alter_address_city_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
