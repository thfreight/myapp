# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-23 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newcar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_color', models.CharField(max_length=50)),
                ('car_wheel_num', models.IntegerField(default=0)),
            ],
        ),
    ]
