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
                                                         availability decimal, news varchar(100),
                                                         squad_number integer)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS PLAYER_BASE_STATS (id integer, points integer,
                                                         minutes integer, cost integer, tsb decimal,
                                                         ppg decimal, goals integer, assists integer,
                                                         cleansheet integer, saves integer, bps integer,
                                                         t_in integer, t_out integer, form decimal)""")
    
    players = get_data("https://fantasy.premierleague.com/drf/elements")
    for player in players:
        position_long = [pos for pos in player_types if pos["id"] == player["element_type"]][0]["singular_name"]
        position_short = [pos for pos in player_types if pos["id"] == player["element_type"]][0]["singular_name_short"]
        availability = None
        if player["chance_of_playing_this_round"] == None:
            availability = 0
        else:
            availability = player["chance_of_playing_this_round"]
        if not player["news"]:
            news = "Match Fit!"
        else:
            news = player["news"]

        cur.execute("""UPDATE PLAYER_INFO SET name=%s, position_short=%s, position_long=%s, team=%s,
                    availability=%s, news=%s, squad_number=%s WHERE id=%s;""", (player["web_name"], 
                    position_short, position_long, player["team"], availability, news, 
                    player["squad_number"], player["id"]))

        cur.execute("""INSERT INTO PLAYER_INFO (id, name, position_short, position_long, team,
                                                availability, news, squad_number)
                    SELECT %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM TEAM_INFO WHERE id=%s)""", (player["id"], 
                    player["web_name"], position_short, position_long, player["team"], 
                    availability, news, player["squad_number"], player["id"]))
    
        cur.execute("""UPDATE PLAYER_BASE_STATS SET points=%s, minutes=%s, cost=%s, tsb=%s,
                    ppg=%s, goals=%s, assists=%s, cleansheet=%s, saves=%s, bps=%s,
                    t_in=%s, t_out=%s, form=%s WHERE id=%s;""", (player["total_points"], 
                    player["minutes"], player["now_cost"]/10, player["selected_by_percent"], 
                    player["points_per_game"], player["goals_scored"], player["assists"], 
                    player["clean_sheets"], player["saves"], player["bps"], 
                    player["transfers_in_event"], player["transfers_out_event"], player["form"], player["id"]))

        cur.execute("""INSERT INTO PLAYER_BASE_STATS (id, points, minutes, cost, tsb,
                                                ppg, goals, assists, cleansheet, saves, bps, t_in, t_out, form)
                    SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM TEAM_INFO WHERE id=%s)""", (player["id"], player["total_points"], 
                    player["minutes"], player["now_cost"]/10, player["selected_by_percent"], 
                    player["points_per_game"], player["goals_scored"], player["assists"], 
                    player["clean_sheets"], player["saves"], player["bps"], 
                    player["transfers_in_event"], player["transfers_out_event"], player["form"], player["id"]))

    
    
    
    conn.commit()
    cur.close()
    return True
