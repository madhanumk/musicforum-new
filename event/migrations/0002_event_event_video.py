# Generated by Django 3.2.2 on 2023-04-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
