# Generated by Django 4.2.11 on 2024-05-28 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_alter_siteconfiguration_favicon_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conf_settings',
            old_name='profile',
            new_name='user',
        ),
    ]
