# Generated by Django 2.1.8 on 2019-05-11 18:49
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar', '0002_auto_20190511_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='weekday',
            name='number',
            field=models.PositiveSmallIntegerField(default=0, unique=True),
        ),
    ]
