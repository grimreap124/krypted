# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-22 19:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eveonline', '0004_auto_20170622_1909'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='expires_on',
            new_name='expires_in',
        ),
    ]
