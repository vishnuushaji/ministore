# Generated by Django 4.2.9 on 2024-02-03 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_order_products_remove_order_total_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Smartphone',
        ),
        migrations.DeleteModel(
            name='Smartwatch',
        ),
    ]
