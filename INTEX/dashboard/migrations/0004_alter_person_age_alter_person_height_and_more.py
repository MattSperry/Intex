# Generated by Django 4.1.2 on 2022-11-29 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_person_personid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='person',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='person',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
