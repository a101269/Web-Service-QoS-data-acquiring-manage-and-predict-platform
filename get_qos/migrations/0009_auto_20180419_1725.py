# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-19 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_qos', '0008_example_base'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example_base',
            name='bandwidth',
            field=models.FloatField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='example_base',
            name='workload',
            field=models.FloatField(blank=True, max_length=50),
        ),
    ]
