# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-04 02:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QoS_attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning', models.CharField(blank=True, max_length=200)),
                ('number', models.IntegerField()),
                ('is_collect', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='QoS_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ws_url', models.CharField(default='www.baidu.com', max_length=200)),
                ('user_ip', models.CharField(default='0.0.0.0', max_length=20)),
                ('http_code', models.CharField(blank=True, max_length=20, null=True)),
                ('namelookup_time', models.FloatField(blank=True, null=True)),
                ('connect_time', models.FloatField(blank=True, null=True)),
                ('pretransfer_time', models.FloatField(blank=True, null=True)),
                ('starttransfer_time', models.FloatField(blank=True, null=True)),
                ('redirect_time', models.FloatField(blank=True, null=True)),
                ('total_time', models.FloatField(blank=True, null=True)),
                ('header_size', models.IntegerField(blank=True, null=True)),
                ('size_download', models.IntegerField(blank=True, null=True)),
                ('size_upload', models.IntegerField(blank=True, null=True)),
                ('speed_download', models.IntegerField(blank=True, null=True)),
                ('speed_upload', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
