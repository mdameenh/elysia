# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 00:32:54 2017

@author: Ameen
"""
'''
PLAYER INFO         : id, name, position_short, position_long, team, availability, news, squad_number
PLAYER_BASE_STATS   : id, points, minutes, cost, tsb, ppg, goals, assists, cleansheet, saves, bps, t_in, t_out, form 
PLAYER_DEEP_STATS   :
TEAM_INFO           : id, name, short_name, next_fixture, difficulty
'''

import os
from urllib import parse
import psycopg2

avail_template = {'a': 'Available', 'i': 'Injured', 'd': 'Doubtful', 'u': 'Unavailable', 's': 'Suspended', 'n': 'Unavailable'}

def generate_table():
    conn = None
    try:        
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])
        
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except Exception as e:
        print(e)

    cur = conn.cursor()
    
    cur.execute("SELECT * FROM fplassist_player_info")
    player_list = []
    player_info = cur.fetchall()
    
    cur.execute("SELECT * FROM fplassist_player_basic_stats")
    player_base_stats = cur.fetchall()
    
    cur.execute("SELECT * FROM fplassist_team_info")
    team_info = cur.fetchall()
    for player in player_info:
        stat = [_stat for _stat in player_base_stats if _stat[0] == player[0]][0]
        team = [_team for _team in team_info if _team[0] == player[4]][0]
        
        player_list.append([player[1], team[2], stat[3], player[2], stat[1], 
                            stat[13], stat[11], stat[12], stat[10], 
                            avail_template[player[5]], stat[8], stat[9], stat[4], stat[2]])
    
        #name, cost, position, points, form, fixture, t_in, t_out, bps, availability, cleansheet, saves, tsb, minutes    
    
    player_list = sorted(player_list, key=lambda x : x[4], reverse=True)
    cur.close()
    return player_list

def update_table(data):
    filter_pos = data.getlist('position[]')
    filter_team = data.getlist('team[]')
    filter_avail = data.getlist('availability[]')
    filter_diff = data.getlist('difficulty[]')
    
    print(data.get('points_min'))
    
    conn = None
    
    try:        
        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])
        
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except Exception as e:
        print(e)

    cur = conn.cursor()
    
    cur.execute("SELECT * FROM fplassist_player_info")
    player_list = []
    player_info = cur.fetchall()
    
    cur.execute("SELECT * FROM fplassist_player_basic_stats")
    player_base_stats = cur.fetchall()
    
    cur.execute("SELECT * FROM fplassist_player_detailed_stats")
    player_deep_stats = cur.fetchall()
    print()
    
    cur.execute("SELECT * FROM fplassist_team_info")
    team_info = cur.fetchall()
    for player in player_info:
        stat = [_stat for _stat in player_base_stats if _stat[0] == player[0]][0]
        team = [_team for _team in team_info if _team[0] == player[4]][0]
        deep_stat = [_stat for _stat in player_deep_stats if _stat[0] == player[0]][0]
        #PLAYER_BASE_STATS   : id0, points1, minutes2, cost3, tsb4, ppg5, goals6, assists7, cleansheet8, saves9, bps10, t_in11, t_out12, form13
        #player_Deep_stats   : id0, ict4, crosses5, chance_created6, clearance7, recover8, key_pass9, tackls10, wingoals11, attemptpass12, comppass13, pen_conced14, chancemiss15, tackld16, offside17, targmiss18, fouls19, dribble20
        if team[1] not in filter_team:
            continue
        elif player[3] not in filter_pos:
            continue
        elif avail_template[player[5]] not in filter_avail:
            continue
        elif stat[1] < int(data.get('points_min')) or stat[1] > int(data.get('points_max')):
            continue
        elif stat[2] < int(data.get('minutes_min')) or stat[2] > int(data.get('minutes_max')):
            continue
        elif stat[3] < float(data.get('price_min')) or stat[3] > float(data.get('price_max')):
            continue
        elif stat[4] < float(data.get('tsb_min')) or stat[4] > float(data.get('tsb_max')):
            continue
        elif stat[5] < float(data.get('ppg_min')) or stat[5] > float(data.get('ppg_max')):
            continue
        elif stat[6] < int(data.get('goals_min')) or stat[6] > int(data.get('goals_max')):
            continue
        elif stat[7] < int(data.get('assists_min')) or stat[7] > int(data.get('assists_max')):
            continue
        elif stat[8] < int(data.get('csheet_min')) or stat[8] > int(data.get('csheet_max')):
            continue
        elif stat[9] < int(data.get('saves_min')) or stat[9] > int(data.get('saves_max')):
            continue
        elif stat[10] < int(data.get('bps_min')) or stat[10] > int(data.get('bps_max')):
            continue
        elif stat[11] < int(data.get('txin_min')) or stat[11] > int(data.get('txin_max')):
            continue
        elif stat[12] < int(data.get('txout_min')) or stat[12] > int(data.get('txout_max')):
            continue
        elif stat[13] < float(data.get('form_min')) or stat[13] > float(data.get('form_max')):
            continue
        elif deep_stat[4] < float(data.get('ict_index_min')) or deep_stat[4] > float(data.get('ict_index_max')):
            continue
        elif deep_stat[5] < int(data.get('open_play_crosses_min')) or deep_stat[5] > int(data.get('open_play_crosses_max')):
            continue
        elif deep_stat[6] < int(data.get('big_chances_created_min')) or deep_stat[6] > int(data.get('big_chances_created_max')):
            continue
        elif deep_stat[7] < int(data.get('clearances_blocks_interceptions_min')) or deep_stat[7] > int(data.get('clearances_blocks_interceptions_max')):
            continue
        elif deep_stat[8] < int(data.get('recoveries_min')) or deep_stat[8] > int(data.get('recoveries_max')):
            continue
        elif deep_stat[9] < int(data.get('key_passes_min')) or deep_stat[9] > int(data.get('key_passes_max')):
            continue
        elif deep_stat[10] < int(data.get('tackles_min')) or deep_stat[10] > int(data.get('tackles_max')):
            continue
        elif deep_stat[11] < int(data.get('winning_goals_min')) or deep_stat[11] > int(data.get('winning_goals_max')):
            continue
        elif deep_stat[12] < int(data.get('attempted_passes_min')) or deep_stat[12] > int(data.get('attempted_passes_max')):
            continue
        elif deep_stat[13] < int(data.get('completed_passes_min')) or deep_stat[13] > int(data.get('completed_passes_max')):
            continue
        elif deep_stat[14] < int(data.get('penalties_conceded_min')) or deep_stat[14] > int(data.get('penalties_conceded_max')):
            continue
        elif deep_stat[15] < int(data.get('big_chances_missed_min')) or deep_stat[15] > int(data.get('big_chances_missed_max')):
            continue
        elif deep_stat[16] < int(data.get('tackled_min')) or deep_stat[16] > int(data.get('tackled_max')):
            continue
        elif deep_stat[17] < int(data.get('offside_min')) or deep_stat[17] > int(data.get('offside_max')):
            continue
        elif deep_stat[18] < int(data.get('target_missed_min')) or deep_stat[18] > int(data.get('target_missed_max')):
            continue
        elif deep_stat[19] < int(data.get('fouls_min')) or deep_stat[19] > int(data.get('fouls_max')):
            continue
        elif deep_stat[20] < int(data.get('dribbles_min')) or deep_stat[20] > int(data.get('dribbles_max')):
            continue

        player_list.append([player[1], team[2], stat[3], player[2], stat[1], 
                            stat[13], stat[11], stat[12], stat[10], 
                            avail_template[player[5]], stat[8], stat[9], stat[4], stat[2]])
    
        #name, cost, position, points, form, fixture, t_in, t_out, bps, availability, cleansheet, saves, tsb, minutes    
    
    player_list = sorted(player_list, key=lambda x : x[4], reverse=True)
    cur.close()
    
    return player_list