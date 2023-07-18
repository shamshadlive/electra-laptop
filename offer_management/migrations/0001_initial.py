# Generated by Django 4.2.2 on 2023-07-18 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoryManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('expire_date', models.DateField()),
                ('discount_percentage', models.IntegerField(default=0)),
                ('category_offer_slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ManyToManyField(to='categoryManagement.category')),
            ],
        ),
    ]