# Generated by Django 4.2.9 on 2024-02-03 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_cartitem_remove_product_stock_remove_product_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Smartphone',
        ),
        migrations.DeleteModel(
            name='Smartwatch',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
