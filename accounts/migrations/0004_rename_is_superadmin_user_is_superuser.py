# Generated by Django 4.2.1 on 2023-06-17 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_latitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_superadmin',
            new_name='is_superuser',
        ),
    ]
