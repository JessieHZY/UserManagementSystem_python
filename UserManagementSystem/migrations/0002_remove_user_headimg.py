# Generated by Django 3.1 on 2020-08-08 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagementSystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='headimg',
        ),
    ]
