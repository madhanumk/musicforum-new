# Generated by Django 3.2.2 on 2023-04-10 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_organizer',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]