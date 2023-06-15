# Generated by Django 4.2.2 on 2023-06-14 12:04

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_on_partner_status_unique_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='instruction',
            field=models.FileField(blank=True, null=True, upload_to=products.models.get_upload_path, verbose_name='Инструкция'),
        ),
    ]