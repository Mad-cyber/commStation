# Generated by Django 4.2.1 on 2023-08-05 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=20, unique=True)),
                ('service_percentage', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Service Percentage %')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]