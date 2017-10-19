# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 19:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FPL_Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bg_active', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Basic_Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('minutes', models.IntegerField(default=0)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=2)),
                ('tsb', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ppg', models.DecimalField(decimal_places=2, max_digits=2)),
                ('goals', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('cleansheet', models.IntegerField(default=0)),
                ('saves', models.IntegerField(default=0)),
                ('bps', models.IntegerField(default=0)),
                ('transfer_in', models.IntegerField(default=0)),
                ('transfer_out', models.IntegerField(default=0)),
                ('form', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Detailed_Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(default=0)),
                ('ict_index', models.DecimalField(decimal_places=2, max_digits=4)),
                ('open_play_crosses', models.IntegerField(default=0)),
                ('big_chances_created', models.IntegerField(default=0)),
                ('clearances_blocks_interceptions', models.IntegerField(default=0)),
                ('recoveries', models.IntegerField(default=0)),
                ('key_passes', models.IntegerField(default=0)),
                ('tackles', models.IntegerField(default=0)),
                ('winning_goals', models.IntegerField(default=0)),
                ('attempted_passes', models.IntegerField(default=0)),
                ('completed_passes', models.IntegerField(default=0)),
                ('penalties_conceded', models.IntegerField(default=0)),
                ('big_chances_missed', models.IntegerField(default=0)),
                ('tackled', models.IntegerField(default=0)),
                ('offside', models.IntegerField(default=0)),
                ('target_missed', models.IntegerField(default=0)),
                ('fouls', models.IntegerField(default=0)),
                ('dribbles', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(default=0)),
                ('player_name', models.CharField(max_length=25)),
                ('pos_short', models.CharField(max_length=4)),
                ('pos_long', models.CharField(max_length=10)),
                ('team_id', models.IntegerField(default=0)),
                ('availability', models.CharField(max_length=2)),
                ('news', models.CharField(max_length=100)),
                ('squad_number', models.IntegerField(default=99)),
            ],
        ),
        migrations.CreateModel(
            name='Team_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField(default=0)),
                ('team_name', models.CharField(max_length=15)),
                ('short_name', models.CharField(max_length=4)),
                ('fixture_difficulty', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
    ]
