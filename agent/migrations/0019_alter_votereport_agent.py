# Generated by Django 5.2.3 on 2025-06-27 01:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0018_rename_polling_station_votereport_poll_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votereport',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote_reports', to='agent.agent'),
        ),
    ]
