# Generated by Django 4.2.1 on 2023-07-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_business_bus_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='bus_slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
