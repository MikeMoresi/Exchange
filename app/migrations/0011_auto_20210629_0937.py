# Generated by Django 3.2.4 on 2021-06-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210628_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='totalsupply',
        ),
        migrations.AddField(
            model_name='profile',
            name='wallet',
            field=models.Field(default=351142.89060510526),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nBTC',
            field=models.IntegerField(default=10),
        ),
    ]
