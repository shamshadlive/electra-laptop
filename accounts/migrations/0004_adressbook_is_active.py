# Generated by Django 4.2.2 on 2023-07-06 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_adressbook_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='adressbook',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]