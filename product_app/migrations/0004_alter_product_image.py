# Generated by Django 4.2.12 on 2025-01-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0003_alter_product_colour"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.TextField(blank=True, null=True),
        ),
    ]
