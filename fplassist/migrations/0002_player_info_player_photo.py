# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fplassist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_info',
            name='player_photo',
            field=models.CharField(default='noimage', max_length=20),
            preserve_default=False,
        ),
    ]
