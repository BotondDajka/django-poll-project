# Generated by Django 3.1.4 on 2020-12-22 12:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_auto_20201222_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='date_lastvote',
        ),
        migrations.AddField(
            model_name='poll',
            name='date_lastvote2',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 22, 12, 53, 33, 221243)),
        ),
        migrations.AlterField(
            model_name='poll',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 22, 12, 53, 33, 221243)),
        ),
    ]
