# Generated by Django 4.2.11 on 2024-05-26 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savedpost',
            old_name='post',
            new_name='posts',
        ),
    ]
