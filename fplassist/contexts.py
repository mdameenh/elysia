# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 00:40:42 2017

@author: Ameen
"""

misc_context = {
            'position' :    ['Goalkeeper', 'Defender', 'Midfielder', 'Forward'],
            
            'team' :        ['Arsenal', 'Bournemouth', 'Brighton', 'Burnley',
                              'Chelsea', 'Crystal Palace', 'Everton', 'Huddersfield', 
                              'Leicester', 'Liverpool', 'Man City', 'Man Utd',
                              'Newcastle', 'Southampton', 'Stoke', 'Swansea', 
                              'Spurs', 'Watford', 'West Brom', 'West Ham'],
                              
            'avail' :       ['Available', 'Doubtful', 'Injured', 'Unavailable'],
            
            'diff' :        ['Very Easy', 'Easy', 'Hard', 'Very Hard'],
            
            'points' :      ['points', '0', '600', '1'],
            'minutes' :     ['minutes', '0', '3600', '1'],
            'price' :       ['price', '0', '15', '0.1'],
            'tsb' :         ['tsb', '0', '100', '0.1'],
            'ppg' :         ['ppg', '0', '30', '0.1'],
            'goals' :       ['goals', '0', '38', '1'],
            'assists' :     ['assists', '0', '38', '1'],
            'csheet' :      ['csheet', '0', '38', '1'],
            'saves' :       ['saves', '0', '200', '1'],
            'txin' :        ['txin', '0', '6000000', '1'],
            'txout' :       ['txout', '0', '6000000', '1'],
            'bps' :         ['bps', '0', '1500', '1'],
            'form' :        ['form', '0', '20', '0.1'],
            
            'ict_index' :                       ['ict_index', '0', '2000', '0.1'], 
            'open_play_crosses' :               ['open_play_crosses', '0', '200', '1'],
            'big_chances_created' :             ['big_chances_created', '0', '200', '1'], 
            'clearances_blocks_interceptions':  ['clearances_blocks_interceptions', '0', '200', '1'],
            'recoveries' :                      ['recoveries', '0', '200', '1'], 
            'key_passes':                       ['key_passes', '0', '200', '1'],
            'tackles' :                         ['tackles', '0', '200', '1'], 
            'winning_goals':                    ['winning_goals', '0', '38', '1'],
            'attempted_passes' :                ['attempted_passes', '0', '10000', '1'], 
            'completed_passes':                 ['completed_passes', '0', '10000', '1'],
            'penalties_conceded' :              ['penalties_conceded', '0', '38', '1'], 
            'big_chances_missed':               ['big_chances_missed', '0', '100', '1'],
            'tackled' :                         ['tackled', '0', '200', '1'], 
            'offside':                          ['offside', '0', '100', '1'],
            'target_missed' :                   ['target_missed', '0', '100', '1'], 
            'fouls':                            ['fouls', '0', '100', '1'],
            'dribbles':                         ['dribbles', '0', '100', '1']
        }

context = {
            'player_info' : [
                                ['position_checkbx', 'pos_div', 'Position', misc_context['position'], 'positions[]'], 
                                ['team_checkbx', 'team_div', 'Team', misc_context['team'], 'team[]'], 
                                ['avail_checkbx', 'avail_div', 'Availability', misc_context['avail'], 'availability[]'], 
                                ['diff_checkbx', 'diff_div', 'Difficulty', misc_context['diff'], 'difficulty[]']
                            ],
                             
            'player_base_stat' : [
                                    ['points_input', 'points_div', 'Points', misc_context['points']],
                                    ['minutes_input', 'minutes_div', 'Minutes', misc_context['minutes']], 
                                    ['price_input', 'price_div', 'Price', misc_context['price']], 
                                    ['tsb_input', 'tsb_div', 'Total Selected By', misc_context['tsb']],
                                    ['ppg_input', 'ppg_div', 'Points Per Game', misc_context['ppg']], 
                                    ['goals_input', 'goals_div', 'Goals', misc_context['goals']], 
                                    ['assists_input', 'assists_div', 'Assists', misc_context['assists']], 
                                    ['csheet_input', 'csheet_div', 'Clean Sheet', misc_context['csheet']], 
                                    ['saves_input', 'saves_div', 'Saves', misc_context['saves']], 
                                    ['txin_input', 'txin_div', 'Transfer-In', misc_context['txin']], 
                                    ['txout_input', 'txout_div', 'Transfer-Out', misc_context['txout']], 
                                    ['bps_input', 'bps_div', 'Bonus Point System', misc_context['bps']], 
                                    ['form_input', 'form_div', 'Form', misc_context['form']]
                                ],
                                  
            'player_deep_stat' : [
                                    ['ict_index_input', 'ict_index_div', 'ICT Index', misc_context['ict_index']],
                                    ['open_play_crosses_input', 'open_play_crosses_div', 'Crosses', misc_context['open_play_crosses']],
                                    ['big_chances_created_input', 'big_chances_created_div', 'Chances Created', misc_context['big_chances_created']],
                                    ['big_chances_missed_input', 'big_chances_missed_div', 'Chances Missed', misc_context['big_chances_missed']],
                                    ['target_missed_input', 'target_missed_div', 'Target Missed', misc_context['recoveries']],
                                    ['clearances_blocks_interceptions_input', 'clearances_blocks_interceptions_div', 'Clearance/Interceptions', misc_context['clearances_blocks_interceptions']],
                                    ['recoveries_input', 'recoveries_div', 'Recoveries', misc_context['recoveries']],
                                    ['tackles_input', 'tackles_div', 'Tackles', misc_context['tackles']],
                                    ['tackled_input', 'tackled_div', 'Tackled', misc_context['tackled']],
                                    ['key_passes_input', 'key_passes_div', 'Key Passes', misc_context['key_passes']],
                                    ['winning_goals_input', 'winning_goals_div', 'Winning Goals', misc_context['winning_goals']],
                                    ['attempted_passes_input', 'attempted_passes_div', 'Attempted Passes', misc_context['attempted_passes']],
                                    ['completed_passes_input', 'completed_passes_div', 'Completed Passes', misc_context['completed_passes']],
                                    ['penalties_conceded_input', 'penalties_conceded_div', 'Penalty Conceded', misc_context['penalties_conceded']],
                                    ['offside_input', 'offside_div', 'Offsides', misc_context['offside']],
                                    ['fouls_input', 'fouls_div', 'Fouls', misc_context['fouls']],
                                    ['dribbles_input', 'dribbles_div', 'Dribbles', misc_context['dribbles']]
                                ],

        }
