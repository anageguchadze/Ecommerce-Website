# Generated by Django 5.0.7 on 2025-01-27 21:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0012_product_image_delete_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='product_app.product')),
            ],
            options={
                'db_table': 'product_image',
            },
        ),
    ]
