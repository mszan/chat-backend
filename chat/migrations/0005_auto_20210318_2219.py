# Generated by Django 3.1.7 on 2021-03-18 22:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_auto_20210318_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(default=None, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]