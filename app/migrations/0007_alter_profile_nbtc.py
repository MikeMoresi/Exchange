# Generated by Django 3.2.4 on 2021-06-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210628_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nBTC',
            field=models.IntegerField(default=6),
        ),
    ]
