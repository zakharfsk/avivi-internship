# Generated by Django 5.0.1 on 2024-02-14 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=255, verbose_name='Brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='colour',
            field=models.CharField(blank=True, max_length=255, verbose_name='Colour'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=255, verbose_name='Size'),
        ),
    ]
