# Generated by Django 4.1.2 on 2022-11-30 23:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_journalentry_date_time_recorded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='date_recorded',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 11, 30, 16, 54, 14, 801410)),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='time_recorded',
            field=models.TimeField(blank=True, default='16:54:14'),
        ),
    ]
