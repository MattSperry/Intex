# Generated by Django 4.1.2 on 2022-11-30 17:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comorbidity',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Comorbidity',
            },
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('food_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('serving_size', models.DecimalField(decimal_places=2, default=1.0, max_digits=6)),
                ('units', models.CharField(max_length=50)),
                ('potassium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('phosphorus', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sodium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('calcium', models.DecimalField(decimal_places=2, max_digits=6)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=6)),
                ('sugar', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'db_table': 'Food',
            },
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('race', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Race',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('personID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('weight', models.IntegerField()),
                ('height', models.IntegerField()),
                ('gender', models.CharField(default='Select', max_length=30)),
                ('comorbidity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.comorbidity')),
                ('race', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.race')),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('journalID', models.AutoField(primary_key=True, serialize=False)),
                ('date_time_recorded', models.DateTimeField(blank=True, default=datetime.datetime(2022, 11, 30, 10, 0, 19, 738246))),
                ('date_time_eaten', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('food_name', models.CharField(max_length=100)),
                ('personID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Journal Entry',
            },
        ),
    ]
