# Generated by Django 4.2.5 on 2023-09-19 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20230713_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_video',
        ),
    ]
