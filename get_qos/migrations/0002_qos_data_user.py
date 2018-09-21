# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-04 02:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('get_qos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qos_data',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]