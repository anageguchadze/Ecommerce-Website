# Generated by Django 4.2.12 on 2025-01-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0002_size_remove_category_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="colour",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
