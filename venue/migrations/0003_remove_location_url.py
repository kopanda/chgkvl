# Generated by Django 2.2.7 on 2019-12-03 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0002_location_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='url',
        ),
    ]
