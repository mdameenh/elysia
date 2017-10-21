# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 00:32:54 2017

@author: Ameen
"""
'''
PLAYER INFO         : (player_id, player_name,pos_short, pos_long,team_id, availability,news)

PLAYER_BASE_STATS   : (player_id, points,minutes, cost, tsb, ppg, goals,assists, cleansheet,saves, bps,transfer_in,transfer_out,form)

PLAYER_DEEP_STATS   : (player_id, ict_index, open_play_crosses,big_chances_created,clearances_blocks_interceptions,recoveries,
                       key_passes,tackles,winning_goals,attempted_passes,completed_passes,penalties_conceded,big_chances_missed,
                       tackled,offside,target_missed,fouls,dribbles,)

TEAM_INFO           : (team_id, team_name, short_name, fixture_difficulty)
'''

from fplassist.models import Team_Info, Player_Info, Player_Basic_Stats, Player_Detailed_Stats

avail_template = {'Available': 'a', 'Injured': 'i', 'Doubtful': 'd', 'Unavailable': ['u', 's', 'n']}
fix_diff_map = {'Very Easy' : 1, 'Easy' : 2, 'Hard' : 3, 'Very Hard' : 4}

def update_table(data):
    filter_pos = data.getlist('positions[]')
    filter_team = data.getlist('team[]')
    filter_avail = data.getlist('availability[]')
    filter_diff = data.getlist('difficulty[]')
    
    print(data.get('points_min'))
    diffs = [fix_diff_map[diff] for diff in filter_diff]
    team_info = Team_Info.objects.filter(team_name__in=filter_team, fixture_difficulty__in=diffs).values()
    team_ids = [team["team_id"] for team in team_info]
    print("#1")
    avail_list = []
    for avail in filter_avail:
        avail_list.extend(avail_template[avail])
    
    print("#2")
    player_info = Player_Info.objects.filter(pos_long__in=filter_pos, team_id__in=team_ids, availability__in=avail_list).values()
    player_id_list = [player["player_id"] for player in player_info]
    print("#3")
    player_base_stats = Player_Basic_Stats.objects.filter(player_id__in=player_id_list, 
                                                          points__gte=data.get('points_min'), points__lte=data.get('points_max'),
                                                          minutes__gte=data.get('minutes_min'), minutes__lte=data.get('minutes_max'),
                                                          cost__gte=data.get('price_min'), cost__lte=data.get('price_max'),
                                                          tsb__gte=data.get('tsb_min'), tsb__lte=data.get('tsb_max'),
                                                          ppg__gte=data.get('ppg_min'), ppg__lte=data.get('ppg_max'),
                                                          goals__gte=data.get('goals_min'), goals__lte=data.get('goals_max'),
                                                          assists__gte=data.get('assists_min'), assists__lte=data.get('assists_max'),
                                                          cleansheet__gte=data.get('csheet_min'), cleansheet__lte=data.get('csheet_max'),
                                                          saves__gte=data.get('saves_min'), saves__lte=data.get('saves_max'),
                                                          transfer_in__gte=data.get('txin_min'), transfer_in__lte=data.get('txin_max'),
                                                          transfer_out__gte=data.get('txout_min'), transfer_out__lte=data.get('txout_max'),
                                                          bps__gte=data.get('bps_min'), bps__lte=data.get('bps_max'),
                                                          form__gte=data.get('form_min'), form__lte=data.get('form_max')                                                          
                                                          ).values()

    player_deep_stats = Player_Detailed_Stats.objects.filter(player_id__in=player_id_list,
                                                             ict_index__gte=data.get('ict_index_min'), ict_index__lte=data.get('ict_index_max'),
                                                             open_play_crosses__gte=data.get('open_play_crosses_min'), open_play_crosses__lte=data.get('open_play_crosses_max'),
                                                             big_chances_created__gte=data.get('big_chances_created_min'), big_chances_created__lte=data.get('big_chances_created_max'),
                                                             big_chances_missed__gte=data.get('big_chances_missed_min'), big_chances_missed__lte=data.get('big_chances_missed_max'),
                                                             recoveries__gte=data.get('recoveries_min'), recoveries__lte=data.get('recoveries_max'),
                                                             clearances_blocks_interceptions__gte=data.get('clearances_blocks_interceptions_min'), 
                                                             clearances_blocks_interceptions__lte=data.get('clearances_blocks_interceptions_max'),
                                                             tackles__gte=data.get('tackles_min'), tackles__lte=data.get('tackles_max'),
                                                             tackled__gte=data.get('tackled_min'), tackled__lte=data.get('tackled_max'),
                                                             key_passes__gte=data.get('key_passes_min'), key_passes__lte=data.get('key_passes_max'),
                                                             winning_goals__gte=data.get('winning_goals_min'), winning_goals__lte=data.get('winning_goals_max'),
                                                             attempted_passes__gte=data.get('attempted_passes_min'), attempted_passes__lte=data.get('attempted_passes_max'),
                                                             completed_passes__gte=data.get('completed_passes_min'), completed_passes__lte=data.get('completed_passes_max'),
                                                             penalties_conceded__gte=data.get('penalties_conceded_min'), penalties_conceded__lte=data.get('penalties_conceded_max'),
                                                             offside__gte=data.get('offside_min'), offside__lte=data.get('offside_max'),
                                                             fouls__gte=data.get('fouls_min'), fouls__lte=data.get('fouls_max'),
                                                             dribbles__gte=data.get('dribbles_min'), dribbles__lte=data.get('dribbles_max'),
                                                             target_missed__gte=data.get('target_missed_min'), target_missed__lte=data.get('target_missed_max'),).values()
    print("###")
    print(len(player_base_stats))
    print(len(player_deep_stats))
    print("###")
    print("#4")
    player_list = []
    for player in player_info:
        #print(player["player_name"])
        team = [_team["team_name"] for _team in team_info if _team["team_id"]==player["team_id"]][0]
        try:
            player_base_stat = [_player for _player in player_base_stats if _player["player_id"]==player["player_id"]][0]
            player_detailed_stat = [_player for _player in player_deep_stats if _player["player_id"]==player["player_id"]][0]
        except IndexError:
            #print("rekt")
            continue
        
        player_list.append([player["player_name"], player["pos_short"], team,
                       player_base_stat["points"], player_base_stat["cost"],
                       player_base_stat["transfer_in"], player_base_stat["transfer_out"],
                       player_base_stat["form"], player_base_stat["minutes"], 
                       player_base_stat["tsb"], player_base_stat["ppg"], 
                       player_base_stat["goals"], player_base_stat["assists"],
                       player_base_stat["cleansheet"], player_base_stat["saves"],
                       player_base_stat["bps"], player_detailed_stat["ict_index"],
                       player_detailed_stat["fouls"],
                         
                        ])
    print("#5")

    #Name 	Position 	Team 	Points Cost Transfer In 	Transfer out Form Minutes TSB PPG goals assist CS saves bps ict fouls
    print("Done")
    return player_list