# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 03:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simon', '0009_auto_20171126_2012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paytype',
            old_name='paytype',
            new_name='pay_type',
        ),
    ]
