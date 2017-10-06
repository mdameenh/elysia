# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 23:12:28 2017

@author: Ameen
"""

# -*- coding: utf-8 -*-
import requests, json, os
import sqlite3
from collections import OrderedDict

player_ceiling_values = {}
team_map = {}

# {team_id : {team_short_name:x,
#              team_difficulty:[0],
#              fixtures:[opponent],
#              location: [home/away],
#              }}

team_fixtures = {}
player_quality_factors = ['now_cost', 'team', 'form', 'total_points', 'threat',
                          'transfers_in_event', 'transfers_out_event', 'bonus', 'saves',
                          'clean_sheets', 'penalties_saved', 'red_cards', 
                          'yellow_cards', 'selected_by_percent', 'minutes']
DATA_AVAIL = True

def get_api_data(api_urls):
    for api_url in api_urls:
        fpl_response = requests.get(api_urls[api_url])
        try:
            fpl_response.raise_for_status()
        except:
            print("Error: There was an error while requesting the http-api. errorcode: %s" % (str(fpl_response.status_code)))
            return False
            
        with open(os.path.join('static/data/', "%s.json"% (api_url)), 'w') as f:
            print("Reading response from url %s" % (fpl_response.url))
            json.dump(fpl_response.json(), f, indent=4)
    return True
    
def get_fixture_difficulty(team_data, event_data, fixture_data):
    for team in team_data:
        team_map[team["id"]] = team["short_name"]

    next_gw = [gw for gw in event_data if gw["is_next"]==True][0]["id"]
    
    fixtures_map = OrderedDict()
    for i in range(next_gw, next_gw+5):
        fixtures_map[i] = [fixture for fixture in fixture_data if fixture["event"] == i]
    
    for team in team_data:
        team_fixtures[team["id"]] = {
                                    "short_name": team["short_name"], 
                                    "opponent_difficulty": [],
                                    "fixtures": [],
                                    "location": [],
                                    }
        for fixtures in fixtures_map:
            for fixture in fixtures_map[fixtures]:
                if fixture["team_h"] == team["id"]:
                    team_fixtures[team["id"]]["fixtures"].append(team_map[fixture["team_a"]])
                    team_fixtures[team["id"]]["location"].append("H")
                    team_fixtures[team["id"]]["opponent_difficulty"].append(fixture["team_h_difficulty"] - fixture["team_a_difficulty"])
                elif fixture["team_a"] == team["id"]:
                    team_fixtures[team["id"]]["fixtures"].append(team_map[fixture["team_h"]])
                    team_fixtures[team["id"]]["location"].append("A")
                    team_fixtures[team["id"]]["opponent_difficulty"].append(fixture["team_a_difficulty"] - fixture["team_h_difficulty"])
        
    return True
    
def get_ceiling_values(player_data):
    for factor in player_quality_factors:
        player_ceiling_values[factor] = float(max(player_data, key=lambda player: float(player[factor]))[factor])
        
    if None in player_ceiling_values.values():
        with open("fpl.log", 'w') as f:
            f.write(player_ceiling_values)
        print("Something doesn't seem right. Check logs")
        return False
    else:
        return True

def update_database():
    print("\n############----------> FPL Helper Script <----------############\n")
    print("Initiating script...\n")
    
    print("Requesting data...")
    with open('static/data/request_urls.json') as url_file:
        get_api_status = get_api_data(json.loads(url_file.read()))
        if not get_api_status:
            return False

    data_files = ['element-types.json', 'events.json', 'fixtures.json',
                  'teams.json', 'elements.json']
    file_missing = False
    for data_file in data_files:
        if os.path.exists(os.path.join('static/data/', data_file)):
            print("Found %s file" % (data_file))
        else:
            print("Could not find file %s" % (data_file))
            file_missing = True
    
    if file_missing:
        print("Some files are missing. Please configure script to request data analyze again\n")
    else:
        print("Necessary files present. Continuing...\n")
    
    print("Generating ceiling values for players...")
    with open('static/data/elements.json') as player_file:
        get_ceiling_status = get_ceiling_values(json.loads(player_file.read()))
        if not get_ceiling_status:
            return False
    
    print("Calculating team difficulties...\n")
    with open('static/data/teams.json') as teams_file:
        with open('static/data/events.json') as events_file:
            with open('static/data/fixtures.json') as fixture_file:
                get_fixture_diff_status = get_fixture_difficulty(json.loads(teams_file.read()),
                                                                 json.loads(events_file.read()),
                                                                 json.loads(fixture_file.read()))
                if not get_fixture_diff_status:
                    return False
    print("Creating internal database with player attributes...")                                                             
    print("Connecting to internal database")
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    print("Calculating player attributes...")
    cursor.execute("DROP TABLE IF EXISTS players")
    cursor.execute("""CREATE TABLE players
    (id, name, cost, cost_n, difficulty, points, points_n, form, form_n,
    threat, threat_n, fixtures, tx_in, tx_in_n, tx_out, tx_out_n, bonus, 
    bonus_n, availability, clean_sheets, clean_sheets_n, penalties_saved, penalties_saved_n, cards, 
    selectedby, selectedby_n, minutes, saves, minutes_n, saves_n, player_type)
    """)
    player_data = []
    with open('static/data/elements.json') as players_file:
        player_data = json.loads(players_file.read())
    
    with open('static/data/element-types.json') as pos_file:
        positions = json.loads(pos_file.read())
    
    
    for player in player_data:
        player_team = team_fixtures[player["team"]]
        fixture_string = ""
        for i in range(len(player_team["fixtures"])):
            fixture_string = fixture_string + "%s [%s], " % (player_team["fixtures"][i],
                                                                    player_team["location"][i])
        difficulty = sum(player_team["opponent_difficulty"])/float(len(player_team["opponent_difficulty"]))
        cards = (player["yellow_cards"]+player["yellow_cards"]) / (player_ceiling_values["yellow_cards"]+player_ceiling_values["yellow_cards"])
        player_position = [position['singular_name'] for position in positions if position['id'] == player['element_type']][0]
        if player["chance_of_playing_next_round"] == None:
            player_chance = 1.0
        else:
            player_chance = player["chance_of_playing_next_round"]/100.0
        
        entry = (player["id"], player["web_name"], player["now_cost"], 
                 player["now_cost"]/player_ceiling_values["now_cost"], 
                 difficulty, player["total_points"], 
                 player["total_points"]/player_ceiling_values["total_points"],
                 float(player["form"]), 
                 float(player["form"])/player_ceiling_values["form"],
                 float(player["threat"]),
                 float(player["threat"])/player_ceiling_values["threat"],
                 fixture_string, player["transfers_in_event"], 
                 player["transfers_in_event"]/player_ceiling_values["transfers_in_event"],
                 player["transfers_out_event"],
                 player["transfers_out_event"]/player_ceiling_values["transfers_out_event"],
                 player["bonus"], 
                 player["bonus"]/player_ceiling_values["bonus"],
                 player_chance, player["clean_sheets"], 
                 player["clean_sheets"]/player_ceiling_values["clean_sheets"],
                 player["penalties_saved"], 
                 player["penalties_saved"]/player_ceiling_values["penalties_saved"],
                 cards, float(player["selected_by_percent"]), 
                 float(player["selected_by_percent"])/player_ceiling_values["selected_by_percent"],
                 player["minutes"], player["saves"], 
                 player["minutes"]/player_ceiling_values["minutes"],
                 player["saves"]/player_ceiling_values["saves"],
                 player_position)
    
    
        cursor.execute("INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", entry)
    
    conn.commit()
    print("Database ready!\n")
    
    return True