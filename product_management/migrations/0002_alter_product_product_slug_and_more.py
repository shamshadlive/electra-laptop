# Generated by Django 4.2.2 on 2023-07-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='product_variant',
            name='product_variant_slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]