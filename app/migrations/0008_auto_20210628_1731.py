# Generated by Django 3.2.4 on 2021-06-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_profile_nbtc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='totalSupply',
        ),
        migrations.AlterField(
            model_name='profile',
            name='nBTC',
            field=models.IntegerField(default=7),
        ),
    ]