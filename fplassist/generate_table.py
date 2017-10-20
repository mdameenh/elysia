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
from fplassist.models import Team_Info, Player_Info, Player_Basic_Stats, Player_Detailed_Stats

avail_template_1 = {'a': 'Available', 'i': 'Injured', 'd': 'Doubtful', 'u': 'Unavailable', 's': 'Unavailable', 'n': 'Unavailable'}
avail_template = {'Available': 'a', 'Injured': 'i', 'Doubtful': 'd', 'Unavailable': ['u', 's', 'n']}

def update_table(data):
    filter_pos = data.getlist('positions[]')
    filter_team = data.getlist('team[]')
    filter_avail = data.getlist('availability[]')
    filter_diff = data.getlist('difficulty[]')
    
    print(data.get('points_min'))
    team_info = Team_Info.objects.filter(team_name__in=filter_team).values()
    team_ids = [team["team_id"] for team in team_info]
    print("#1")
    avail_list = []
    for avail in filter_avail:
        avail_list.extend(avail_template[avail])
    
    print("#2")
    player_info = Player_Info.objects.filter(pos_long__in=filter_pos, team_id__in=team_ids, availability__in=avail_list).values()
    player_id_list = [player["player_id"] for player in player_info]
    print("#3")
    player_base_stats = Player_Basic_Stats.objects.filter(player_id__in=player_id_list).values()
    print("#4")
    player_list = []
    for player in player_info:
        print(player["player_name"])
        team = [_team["team_name"] for _team in team_info if _team["team_id"]==player["team_id"]][0]
        player_base_stat = [_player for _player in player_base_stats if _player["player_id"]==player["player_id"]][0]
        player_list.append([player["player_name"], team,
                       player_base_stat["cost"], player["pos_short"], 
                       player_base_stat["points"], player_base_stat["form"],
                       player_base_stat["transfer_in"], player_base_stat["transfer_out"],
                       player_base_stat["bps"], player["availability"], 
                       player_base_stat["cleansheet"], player_base_stat["saves"], 
                       player_base_stat["tsb"], player_base_stat["minutes"]])
    print("#5")
    #Name 	Team 	Cost 	Position 	Points 	Form 	Transfer In 	Transfer out 	Bonus 	Availability 	CleanSheet 	Saves 	Selected By 	Minutes
    print("Done")
    return sorted(player_list, key=lambda x : x[4], reverse=True)


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
        stat = [_stat for _stat in player_base_stats if _stat[1] == player[1]][0]
        team = [_team for _team in team_info if _team[1] == player[5]][0]
        
        player_list.append([player[2], team[3], stat[4], player[3], stat[2], 
                            stat[14], stat[12], stat[13], stat[11], 
                            avail_template_1[player[6]], stat[9], stat[10], stat[5], stat[3]])
    
        #name, cost, position, points, form, fixture, t_in, t_out, bps, availability, cleansheet, saves, tsb, minutes    
    
    player_list = sorted(player_list, key=lambda x : x[4], reverse=True)
    cur.close()
    return player_list

