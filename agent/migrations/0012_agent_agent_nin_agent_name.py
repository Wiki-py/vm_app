# Generated by Django 5.2.3 on 2025-06-26 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0011_alter_incident_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='agent_nin',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='agent',
            name='name',
            field=models.CharField(default='Agent', max_length=100, null=True),
        ),
    ]
