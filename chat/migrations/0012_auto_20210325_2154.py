# Generated by Django 3.1.7 on 2021-03-25 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_auto_20210322_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.TextField(max_length=50, unique=True),
        ),
    ]
