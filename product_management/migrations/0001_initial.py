# Generated by Django 4.2.2 on 2023-07-05 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoryManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atribute_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Atribute_Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atribute_value', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('atribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.atribute')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_slug', models.SlugField(blank=True, unique=True)),
                ('product_description', models.TextField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product_management.brand')),
                ('product_catg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categoryManagement.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.CharField(max_length=30)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.IntegerField()),
                ('product_variant_slug', models.SlugField(blank=True, unique=True)),
                ('thumbnail_image', models.ImageField(upload_to='product_variant/images/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('atributes', models.ManyToManyField(related_name='attributes', to='product_management.atribute_value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.product')),
            ],
        ),
        migrations.CreateModel(
            name='Additional_Product_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_variant/additional/images/')),
                ('is_active', models.BooleanField(default=True)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_product_images', to='product_management.product_variant')),
            ],
        ),
        migrations.AddConstraint(
            model_name='product_variant',
            constraint=models.UniqueConstraint(condition=models.Q(('sku_id__isnull', False)), fields=('product', 'sku_id'), name='Unique skuid must be provided'),
        ),
    ]
