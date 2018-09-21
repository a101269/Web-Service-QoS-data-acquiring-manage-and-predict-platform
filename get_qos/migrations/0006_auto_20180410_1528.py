# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-10 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_qos', '0005_auto_20180406_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor_setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_interval', models.IntegerField(blank=True, default=30)),
            ],
        ),
        migrations.AddField(
            model_name='qos_data',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
