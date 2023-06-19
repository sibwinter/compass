# Generated by Django 4.2.2 on 2023-06-19 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0002_alter_partner_options_and_more'),
        ('products', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_on_partner_status',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner_status', to='partners.partner', verbose_name='Партнер'),
        ),
        migrations.AlterField(
            model_name='product_on_partner_status',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partner_status', to='products.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='product_on_partner_status',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Залит на сайт'),
        ),
    ]
