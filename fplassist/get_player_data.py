# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:07:19 2017

@author: Ameen
"""

from fplassist.models import Team_Info, Player_Info, Player_Basic_Stats, Player_Detailed_Stats

avail_map = {'a': 'Available', 'i': 'Injured', 'd': 'Doubtful', 
             'u': 'Unavailable', 's': 'Unavailable', 'n': 'Unavailable', }
difficulty_map = {1: 'Very Easy', 2: 'Easy', 3: 'Hard', 4: 'Very Hard'}

def get_player_data(data):
    team_info = Team_Info.objects.all()
    info_table = Player_Info.objects.all()
    base_stat_table = Player_Basic_Stats.objects.all()
    deep_stat_table = Player_Detailed_Stats.objects.all()
    
    player_data = []
    
    for player in info_table:
        _tmpPlayer = {}
        _tmpPlayer["id"] = player.player_id
        _tmpPlayer["name"] = player.player_name
        _tmpPlayer["position"] = player.pos_long
        _tmpTeam = [team for team in team_info if team.team_id==player.team_id][0]
        _tmpPlayer["team"] = _tmpTeam.team_name
        _tmpPlayer["availability"] = avail_map[player.availability]
        _tmpPlayer["difficulty"] = difficulty_map[_tmpTeam.fixture_difficulty]
        
        base_stat = [_player for _player in base_stat_table if _player.player_id==player.player_id][0]
        
        _tmpPlayer["points"] = base_stat.points
        _tmpPlayer["minutes"] = base_stat.minutes
        _tmpPlayer["price"] = float(base_stat.cost)
        _tmpPlayer["tsb"] = float(base_stat.tsb)
        _tmpPlayer["ppg"] = float(base_stat.ppg)
        _tmpPlayer["goals"] = base_stat.goals
        _tmpPlayer["assists"] = base_stat.assists
        _tmpPlayer["cleansheets"] = base_stat.cleansheet
        _tmpPlayer["saves"] = base_stat.saves
        _tmpPlayer["transfer-in"] = base_stat.transfer_in
        _tmpPlayer["transfer-out"] = base_stat.transfer_out
        _tmpPlayer["bps"] = base_stat.bps
        _tmpPlayer["form"] = float(base_stat.form)
        
        deep_stat = [_player for _player in deep_stat_table if _player.player_id==player.player_id][0]
        
        _tmpPlayer["ict-index"] = float(deep_stat.ict_index)
        _tmpPlayer["crosses"] = deep_stat.open_play_crosses
        _tmpPlayer["chances-created"] = deep_stat.big_chances_created
        _tmpPlayer["chances-missed"] = deep_stat.big_chances_missed
        _tmpPlayer["target-missed"] = deep_stat.target_missed
        _tmpPlayer["clearance-block"] = deep_stat.clearances_blocks_interceptions
        _tmpPlayer["recoveries"] = deep_stat.recoveries
        _tmpPlayer["tackles"] = deep_stat.tackles
        _tmpPlayer["tackled"] = deep_stat.tackled
        _tmpPlayer["key-passes"] = deep_stat.key_passes
        _tmpPlayer["winning-goals"] = deep_stat.winning_goals
        _tmpPlayer["attempted-passes"] = deep_stat.attempted_passes
        _tmpPlayer["completed-passes"] = deep_stat.completed_passes
        _tmpPlayer["penalties-conceded"] = deep_stat.penalties_conceded
        _tmpPlayer["offside"] = deep_stat.offside
        _tmpPlayer["fouls"] = deep_stat.fouls
        _tmpPlayer["dribbles"] = deep_stat.dribbles
        _tmpPlayer["points-history"] = deep_stat.points_history
        _tmpPlayer["ict-index-history"] = deep_stat.ict_history
        
        player_data.append(_tmpPlayer)
    
    return sorted(player_data, key=lambda x : x["points"], reverse=True)    