from django.db import models
from datetime import datetime
# Create your models here.
class Team_Info(models.Model):
    team_id = models.IntegerField(default=0)
    team_name = models.CharField(max_length=15)
    short_name = models.CharField(max_length=4)
    fixture_difficulty = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __str__(self):
        return self.team_name
    
class Player_Info(models.Model):
    player_id = models.IntegerField(default=0)
    player_name = models.CharField(max_length=25)
    pos_short = models.CharField(max_length=4)
    pos_long = models.CharField(max_length=10)
    team_id = models.IntegerField(default=0)
    availability = models.CharField(max_length=2)
    news = models.CharField(max_length=100)
    
    def __str__(self):
        return self.player_name

class Player_Basic_Stats(models.Model):
    player_id = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=4, decimal_places=2)
    tsb = models.DecimalField(max_digits=4, decimal_places=2)
    ppg = models.DecimalField(max_digits=4, decimal_places=2)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    cleansheet = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    bps = models.IntegerField(default=0)
    transfer_in = models.IntegerField(default=0)
    transfer_out = models.IntegerField(default=0)
    form = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __str__(self):
        return self.player_id

class Player_Detailed_Stats(models.Model):
    player_id = models.IntegerField(default=0)
    ict_index = models.DecimalField(max_digits=5, decimal_places=2)
    open_play_crosses = models.IntegerField(default=0)
    big_chances_created = models.IntegerField(default=0)
    clearances_blocks_interceptions = models.IntegerField(default=0)
    recoveries = models.IntegerField(default=0)
    key_passes = models.IntegerField(default=0)
    tackles = models.IntegerField(default=0)
    winning_goals = models.IntegerField(default=0)
    attempted_passes = models.IntegerField(default=0)
    completed_passes = models.IntegerField(default=0)
    penalties_conceded = models.IntegerField(default=0)
    big_chances_missed = models.IntegerField(default=0)
    tackled = models.IntegerField(default=0)
    offside = models.IntegerField(default=0)
    target_missed = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    dribbles = models.IntegerField(default=0)

    def __str__(self):
        return self.player_id
    
class FPL_Config(models.Model):
    bg_active = models.BooleanField(default=False)
    last_updated = models.DateTimeField(blank=True, auto_now_add=True)