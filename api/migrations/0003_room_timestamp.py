# Generated by Django 3.1.7 on 2021-04-03 17:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210403_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 4, 3, 17, 15, 8, 414847, tzinfo=utc)),
            preserve_default=False,
        ),
    ]