# Generated by Django 3.1.4 on 2020-12-11 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sync', '0004_mediaserver_server_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediaserver',
            name='valid',
        ),
    ]