# Generated by Django 3.2.4 on 2021-06-28 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_profile_nbtc'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='totalSupply',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nBTC',
            field=models.IntegerField(default=None),
        ),
    ]