# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-10 07:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('get_qos', '0006_auto_20180410_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qos_data',
            name='add_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]