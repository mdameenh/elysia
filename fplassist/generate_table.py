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
    
    cur.execute("SELECT * FROM player_info")
    player_list = []
    player_info = cur.fetchall()
    
    cur.execute("SELECT * FROM player_base_stats")
    player_base_stats = cur.fetchall()
    
    cur.execute("SELECT * FROM team_info")
    team_info = cur.fetchall()
    
    for player in player_info:
        stat = [_stat for _stat in player_base_stats if _stat[0] == player[0]][0]
        team = [_team for _team in team_info if _team[0] == player[4]][0]
        
        player_list.append([player[1], team[2], stat[3], player[2], stat[1], 
                            stat[13], stat[11], stat[12], stat[10], 
                            player[5], stat[8], stat[9], stat[4], stat[2]])
    
        #name, cost, position, points, form, fixture, t_in, t_out, bps, availability, cleansheet, saves, tsb, minutes    
    
    player_list = sorted(player_list, key=lambda x : x[4], reverse=True)
    cur.close()
    return player_list[:50]

def update_table(data):
    print(data)
    return data.getlist('checks[]')
    