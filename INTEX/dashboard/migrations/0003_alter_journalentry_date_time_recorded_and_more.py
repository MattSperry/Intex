# Generated by Django 4.1.2 on 2022-11-30 22:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_journalentry_date_time_recorded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='date_time_recorded',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 30, 15, 52, 19, 614797)),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]