# Generated by Django 3.1.4 on 2020-12-22 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0014_auto_20201222_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='date_lastvote',
            field=models.DateTimeField(null=True),
        ),
    ]
