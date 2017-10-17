# -*- coding: utf-8 -*-
import requests, os

from urllib import parse
import psycopg2

def get_data(api_url):
    api_response = requests.get(api_url)
    try:
        api_response.raise_for_status()
        api_data = api_response.json()
    except:
        print("Error: There was an error while requesting the http-api. \
              errorcode: %s" % (str(api_response.status_code)))
        return False

    if api_data:
        return api_data
    else:
        return False
    

def update_database():
    print("\n############----------> FPL Helper Script <----------############\n")
    print("Initiating script...\n")

    print("Connecting to database...")
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    
    cur = conn.cursor()
    print("Connection Successful...")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS TEAM_INFO (id integer, name varchar(15), short_name varchar(4),
                                                         next_fixture varchar(45), difficulty decimal)""")
    
    print("Identifying next game week...")
    event_data = get_data("https://fantasy.premierleague.com/drf/events")

    next_gameweek = [gw for gw in event_data if gw["is_next"] == True][0]["id"]
    if next_gameweek == None:
        print("There was a problem identifying next game week!")
        return False
    

    print("Collecting team information...")
    team_data = get_data("https://fantasy.premierleague.com/drf/teams")
    
    print("Collecting fixture information...")
    fixture_data = get_data("https://fantasy.premierleague.com/drf/fixtures")
    
    for team in team_data:
        next_fixtures = []
        difficulty = 0
        for gameweek in range(next_gameweek, next_gameweek+5):
            fixtures = [fixture for fixture in fixture_data if fixture["event"] == gameweek]
            for fixture in fixtures:
                if fixture["team_h"] == team["id"]:
                    next_fixtures.append("%s [H]" %(fixture["team_a"]))
                    difficulty += (fixture["team_h_difficulty"] - fixture["team_a_difficulty"])
                elif fixture["team_a"] == team["id"]:
                    next_fixtures.append("%s [A]" %(fixture["team_h"]))
                    difficulty += (fixture["team_a_difficulty"] - fixture["team_h_difficulty"])
                
        cur.execute("""UPDATE TEAM_INFO SET name=%s, short_name=%s, next_fixture=%s, 
                    difficulty=%s WHERE id=%s;""", (team["name"], team["short_name"], ", ".join(next_fixtures),
                    ""+str(difficulty/5.0), team["id"]))
                    
        cur.execute("""INSERT INTO TEAM_INFO (id, name, short_name, next_fixture, difficulty)
                    SELECT %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM TEAM_INFO WHERE id=%s)""", (team["id"], 
                    team["name"], team["short_name"], ", ".join(next_fixtures), difficulty/5.0, team["id"]))
    
    print("Fixtures and team information stored successfully!")
    
    print("Collecting player information...")
    player_types = get_data("https://fantasy.premierleague.com/drf/element-types")

    print("Collecting player base stats...")

    cur.execute("""CREATE TABLE IF NOT EXISTS PLAYER_INFO (id integer, name varchar(25),
                                                         position_short varchar(4), position_long varchar(10), team integer,
                                                         availability varchar(2), news varchar(100),
                                                         squad_number integer)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS PLAYER_BASE_STATS (id integer, points integer,
                                                         minutes integer, cost decimal, tsb decimal,
                                                         ppg decimal, goals integer, assists integer,
                                                         cleansheet integer, saves integer, bps integer,
                                                         t_in integer, t_out integer, form decimal)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS PLAYER_DEEP_STATS (id integer, influence decimal,
                                                         creativity decimal, threat decimal, ict_index decimal,
                                                         open_play_crosses integer, big_chances_created integer, clearances_blocks_interceptions integer,
                                                         recoveries integer, key_passes integer, tackles integer,
                                                         winning_goals integer, attempted_passes integer, completed_passes integer,
                                                         penalties_conceded integer, big_chances_missed integer, tackled integer,
                                                         offside integer, target_missed integer, fouls integer, 
                                                         dribbles integer)""")
    
    players = get_data("https://fantasy.premierleague.com/drf/elements")
    for player in players:
        player_cost = "%.1f" % (int(player["now_cost"])/10.0)
        position_long = [pos for pos in player_types if pos["id"] == player["element_type"]][0]["singular_name"]
        position_short = [pos for pos in player_types if pos["id"] == player["element_type"]][0]["singular_name_short"]

        if not player["news"]:
            news = "Match Fit!"
        else:
            news = player["news"]

        player_deep_cumul = {'influence':0, 'creativity':0, 'threat':0, 'ict_index':0,
                            'open_play_crosses':0, 'big_chances_created':0, 'clearances_blocks_interceptions':0, 'recoveries':0, 
                            'key_passes':0, 'tackles':0, 'winning_goals':0, 'attempted_passes':0, 'completed_passes':0,
                            'penalties_conceded':0, 'big_chances_missed':0, 'tackled':0, 'offside':0, 
                            'target_missed':0, 'fouls':0, 'dribbles':0}
        
        player_deep = get_data("https://fantasy.premierleague.com/drf/element-summary/%d" % (player["id"]))["history"]
        for deep_stat in player_deep:
            for deep_attr in player_deep_cumul:
                print(deep_attr)
                print(deep_stat[deep_attr])
                player_deep_cumul[deep_attr] +=  float(deep_stat[deep_attr])

        cur.execute("""UPDATE PLAYER_INFO SET name=%s, position_short=%s, position_long=%s, team=%s,
                    availability=%s, news=%s, squad_number=%s WHERE id=%s;""", (player["web_name"], 
                    position_short, position_long, player["team"], player["status"], news, 
                    player["squad_number"], player["id"]))

        cur.execute("""INSERT INTO PLAYER_INFO (id, name, position_short, position_long, team,
                                                availability, news, squad_number)
                    SELECT %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM PLAYER_INFO WHERE id=%s)""", (player["id"], 
                    player["web_name"], position_short, position_long, player["team"], 
                    player["status"], news, player["squad_number"], player["id"]))
    
        cur.execute("""UPDATE PLAYER_BASE_STATS SET points=%s, minutes=%s, cost=%s, tsb=%s,
                    ppg=%s, goals=%s, assists=%s, cleansheet=%s, saves=%s, bps=%s,
                    t_in=%s, t_out=%s, form=%s WHERE id=%s;""", (player["total_points"], 
                    player["minutes"], player_cost, player["selected_by_percent"], 
                    player["points_per_game"], player["goals_scored"], player["assists"], 
                    player["clean_sheets"], player["saves"], player["bps"], 
                    player["transfers_in_event"], player["transfers_out_event"], player["form"], player["id"]))

        cur.execute("""INSERT INTO PLAYER_BASE_STATS (id, points, minutes, cost, tsb,
                                                ppg, goals, assists, cleansheet, saves, bps, t_in, t_out, form)
                    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM PLAYER_BASE_STATS WHERE id=%s)""", (player["id"], player["total_points"], 
                    player["minutes"], player_cost, player["selected_by_percent"], 
                    player["points_per_game"], player["goals_scored"], player["assists"], 
                    player["clean_sheets"], player["saves"], player["bps"], 
                    player["transfers_in_event"], player["transfers_out_event"], player["form"], player["id"]))
        
        cur.execute("""UPDATE PLAYER_DEEP_STATS SET influence=%s, creativity=%s, threat=%s, ict_index=%s,
                    open_play_crosses=%s, big_chances_created=%s, clearances_blocks_interceptions=%s, recoveries=%s, key_passes=%s, tackles=%s,
                    winning_goals=%s, attempted_passes=%s, completed_passes=%s, penalties_conceded=%s,
                    big_chances_missed=%s, tackled=%s, offside=%s, target_missed=%s,
                    fouls=%s, dribbles=%s WHERE id=%s;""", (player_deep_cumul["influence"], 
                    player_deep_cumul["creativity"], player_deep_cumul["threat"], player_deep_cumul["ict_index"], 
                    int(player_deep_cumul["open_play_crosses"]), int(player_deep_cumul["big_chances_created"]), int(player_deep_cumul["clearances_blocks_interceptions"]), 
                    int(player_deep_cumul["recoveries"]), int(player_deep_cumul["key_passes"]), int(player_deep_cumul["tackles"]), 
                    int(player_deep_cumul["winning_goals"]), int(player_deep_cumul["attempted_passes"]), int(player_deep_cumul["completed_passes"]), 
                    int(player_deep_cumul["penalties_conceded"]), int(player_deep_cumul["big_chances_missed"]), int(player_deep_cumul["tackled"]), 
                    int(player_deep_cumul["offside"]), int(player_deep_cumul["target_missed"]), int(player_deep_cumul["fouls"]), 
                    int(player_deep_cumul["dribbles"]), player_deep_cumul["id"]))

        cur.execute("""INSERT INTO PLAYER_DEEP_STATS (id, influence, creativity, threat, ict_index,
                                                open_play_crosses, big_chances_created, clearances_blocks_interceptions, recoveries, 
                                                key_passes, tackles, winning_goals, attempted_passes, completed_passes,
                                                penalties_conceded, big_chances_missed, tackled, offside, 
                                                target_missed, fouls, dribbles)
                    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM PLAYER_BASE_STATS WHERE id=%s)""", (player["id"], player_deep_cumul["influence"], 
                    player_deep_cumul["creativity"], player_deep_cumul["threat"], player_deep_cumul["ict_index"], 
                    int(player_deep_cumul["open_play_crosses"]), int(player_deep_cumul["big_chances_created"]), 
                    int(player_deep_cumul["clearances_blocks_interceptions"]), int(player_deep_cumul["recoveries"]), 
                    int(player_deep_cumul["key_passes"]),int( player_deep_cumul["tackles"]), int(player_deep_cumul["winning_goals"]), 
                    int(player_deep_cumul["attempted_passes"]), int(player_deep_cumul["completed_passes"]), 
                    int(player_deep_cumul["penalties_conceded"]), int(player_deep_cumul["big_chances_missed"]), 
                    int(player_deep_cumul["tackled"]), int(player_deep_cumul["offside"]), int(player_deep_cumul["target_missed"]), 
                    int(player_deep_cumul["fouls"]), int(player_deep_cumul["dribbles"]), player["id"]))
    
    
    conn.commit()
    cur.close()
    return True
