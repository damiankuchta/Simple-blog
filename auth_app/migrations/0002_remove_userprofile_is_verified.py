# Generated by Django 3.0.5 on 2020-04-22 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_verified',
        ),
    ]