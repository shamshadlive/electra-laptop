# Generated by Django 4.2.2 on 2023-07-03 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=50, unique=True)),
                ('cat_slug', models.SlugField(blank=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('parent_cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categoryManagement.category')),
            ],
        ),
    ]
