# -*- coding: utf-8 -*-
import requests
from datetime import datetime
from fplassist.models import Team_Info, Player_Info, Player_Basic_Stats, Player_Detailed_Stats, FPL_Config

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
        difficulty = 0
        for gameweek in range(next_gameweek, next_gameweek+5):
            fixtures = [fixture for fixture in fixture_data if fixture["event"] == gameweek]
            for fixture in fixtures:
                if fixture["team_h"] == team["id"]:
                    difficulty += (fixture["team_h_difficulty"] - fixture["team_a_difficulty"])
                elif fixture["team_a"] == team["id"]:
                    difficulty += (fixture["team_a_difficulty"] - fixture["team_h_difficulty"])
        
        team_entry = Team_Info(team_id=team["id"], team_name=team["name"], 
                               short_name=team["short_name"], 
                               fixture_difficulty=difficulty/5.0)
        team_entry.save()
    
    print("Team and Fixture Difficulty information stored successfully!")
    
    print("Collecting player information...")
    player_types = get_data("https://fantasy.premierleague.com/drf/element-types")

    print("Collecting player base stats...")
    
    players = get_data("https://fantasy.premierleague.com/drf/elements")
    for player in players:
        print(player["web_name"])
        player_cost = "%.1f" % (int(player["now_cost"])/10.0)
        position_long = [pos for pos in player_types if pos["id"] == player["element_type"]][0]["singular_name"]
        position_short = [pos for pos in player_types if pos["id"] == player["element_type"]][0]["singular_name_short"]

        if not player["news"]:
            p_news = "Match Fit!"
        else:
            p_news = player["news"]

        player_deep_cumul = {'influence':0, 'creativity':0, 'threat':0, 'ict_index':0,
                            'open_play_crosses':0, 'big_chances_created':0, 'clearances_blocks_interceptions':0, 'recoveries':0, 
                            'key_passes':0, 'tackles':0, 'winning_goals':0, 'attempted_passes':0, 'completed_passes':0,
                            'penalties_conceded':0, 'big_chances_missed':0, 'tackled':0, 'offside':0, 
                            'target_missed':0, 'fouls':0, 'dribbles':0}
        
        player_deep = get_data("https://fantasy.premierleague.com/drf/element-summary/%d" % (player["id"]))["history"]
        for deep_stat in player_deep:
            for deep_attr in player_deep_cumul:
                player_deep_cumul[deep_attr] +=  float(deep_stat[deep_attr])
        
        player_info = Player_Info(player_id=player["id"], player_name=player["web_name"],
                                  pos_short=position_short, pos_long=position_long,
                                  team_id=player["team"], availability=player["status"],
                                  news=p_news, squad_number=player["squad_number"])
        player_info.save()
        
        player_base_stats = Player_Basic_Stats(player_id=player["id"], points=player["total_points"],
                                               minutes=player["minutes"], cost=player_cost, 
                                               tsb=player["selected_by_percent"], 
                                               ppg=player["points_per_game"], goals=player["goals_scored"],
                                               assists=player["assists"], cleansheet=player["clean_sheets"],
                                               saves=player["saves"], bps=player["bps"],
                                               transfer_in=player["transfers_in_event"],
                                               transfer_out=player["transfers_out_event"],
                                               form=player["form"])
        player_base_stats.save()
        
        player_detailed = Player_Detailed_Stats(player_id=player["id"], ict_index=player_deep_cumul["ict_index"],
                                                open_play_crosses=player_deep_cumul["open_play_crosses"],
                                                big_chances_created=player_deep_cumul["big_chances_created"],
                                                clearances_blocks_interceptions=player_deep_cumul["clearances_blocks_interceptions"],
                                                recoveries=player_deep_cumul["recoveries"],
                                                key_passes=player_deep_cumul["key_passes"],
                                                tackles=player_deep_cumul["tackles"],
                                                winning_goals=player_deep_cumul["winning_goals"],
                                                attempted_passes=player_deep_cumul["attempted_passes"],
                                                completed_passes=player_deep_cumul["completed_passes"],
                                                penalties_conceded=player_deep_cumul["penalties_conceded"],
                                                big_chances_missed=player_deep_cumul["big_chances_missed"],
                                                tackled=player_deep_cumul["tackled"],
                                                offside=player_deep_cumul["offside"],
                                                target_missed=player_deep_cumul["target_missed"],
                                                fouls=player_deep_cumul["fouls"],
                                                dribbles=player_deep_cumul["dribbles"])
        player_detailed.save()

    p = FPL_Config.objects.filter(id=1)
    p.bg_active = False
    p.last_updated = datetime.now()
    p.save()
    
    return