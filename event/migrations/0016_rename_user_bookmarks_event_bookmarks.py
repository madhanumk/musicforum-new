# Generated by Django 5.0.6 on 2024-07-06 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0015_remove_event_participants_event_user_bookmarks_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='user_bookmarks',
            new_name='bookmarks',
        ),
    ]
