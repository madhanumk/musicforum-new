# Generated by Django 5.0.6 on 2024-07-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_remove_event_likes_remove_event_user_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_video',
            field=models.URLField(blank=True, null=True),
        ),
    ]