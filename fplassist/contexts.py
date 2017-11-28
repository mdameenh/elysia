# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 00:40:42 2017

@author: Ameen
"""

filter_data = {
            "player_info" : [
                        {
                            "name" : "Position",
                            "values" : ["Goalkeeper", "Defender", "Midfielder", "Forward"]
                        },
                        {
                            "name" : "Team",
                            "values" : ['Arsenal', 'Bournemouth', 'Brighton', 
                                        'Burnley', 'Chelsea', 'Crystal Palace',
                                        'Everton', 'Huddersfield', 'Leicester',
                                        'Liverpool', 'Man City', 'Man Utd',
                                        'Newcastle', 'Southampton', 'Stoke', 
                                        'Swansea', 'Spurs', 'Watford', 
                                        'West Brom', 'West Ham']
                        },
                        {
                            "name" : "Availability",
                            "values": ['Available', 'Doubtful', 'Injured', 
                                       'Unavailable']
                        },
                        {
                            "name" : "Difficulty",
                            "values" : ['Very Easy', 'Easy', 'Hard', 
                                        'Very Hard']
                        }
                    ],
            "player_base" : [
                        {
                          "name" : "Points",
                          "values" : {
                                      "min" : -100,
                                      "max" : 600,
                                      "step" : 1
                                  }
                        },

                        {
                          "name" : "Minutes",
                          "values" : {
                                      "min" : 0,
                                      "max" : 3600,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Price",
                          "values" : {
                                      "min" : 0,
                                      "max" : 15,
                                      "step" : 0.1
                                  }
                        },
                        {
                          "name" : "TSB",
                          "values" : {
                                      "min" : 0,
                                      "max" : 100,
                                      "step" : 0.1
                                  }
                        },
                        {
                          "name" : "PPG",
                          "values" : {
                                      "min" : -100,
                                      "max" : 600,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Goals",
                          "values" : {
                                      "min" : 0,
                                      "max" : 38,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Assists",
                          "values" : {
                                      "min" : 0,
                                      "max" : 38,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "CleanSheets",
                          "values" : {
                                      "min" : 0,
                                      "max" : 38,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Saves",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Transfer-In",
                          "values" : {
                                      "min" : 0,
                                      "max" : 6000000,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Transfer-Out",
                          "values" : {
                                      "min" : 0,
                                      "max" : 6000000,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "BPS",
                          "values" : {
                                      "min" : -100,
                                      "max" : 1500,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Form",
                          "values" : {
                                      "min" : -10,
                                      "max" : 20,
                                      "step" : 0.1
                                  }
                        },

                    
                    ],
            "player_deep" : [
                        {
                          "name" : "ICT-Index",
                          "values" : {
                                      "min" : 0,
                                      "max" : 2000,
                                      "step" : 0.1
                                  }
                        },

                        {
                          "name" : "Crosses",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Chances-Created",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Chances-Missed",
                          "values" : {
                                      "min" : 0,
                                      "max" : 100,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Target-Missed",
                          "values" : {
                                      "min" : 0,
                                      "max" : 100,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Clearance-Block",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Recoveries",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Tackles",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Tackled",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Key-Passes",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Winning-Goals",
                          "values" : {
                                      "min" : 0,
                                      "max" : 38,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Attempted-Passes",
                          "values" : {
                                      "min" : 0,
                                      "max" : 9999,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Completed-Passes",
                          "values" : {
                                      "min" : 0,
                                      "max" : 9999,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Penalties-Conceded",
                          "values" : {
                                      "min" : 0,
                                      "max" : 38,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Offside",
                          "values" : {
                                      "min" : 0,
                                      "max" : 100,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Fouls",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                        {
                          "name" : "Dribbles",
                          "values" : {
                                      "min" : 0,
                                      "max" : 200,
                                      "step" : 1
                                  }
                        },
                    
                    ],
            "misc_options" : [
                        {
                            "name" : "Columns",
                            "values" : ["Position", "Team", "Availability", 
                                        "Difficulty", "Points", "Minutes", 
                                        "Price", "TSB", "PPG", "Goals", 
                                        "Assists", "Cleansheets", "Saves", 
                                        "Transfer-In", "Transfer-Out", 
                                        "BPS", "Form", "ICT-Index", "Crosses", 
                                        "Chances-Created", "Chances-Missed", 
                                        "Target-Missed", "Clearance-Block", "Recoveries", 
                                        "Tackles", "Tackled", "Key-Passes", 
                                        "Winning-Goals", "Attempted-Passes", 
                                        "Completed-Passes", "Penalties-Conceded", 
                                        "Offside", "Fouls", "Dribbles"]
                        },
                    ],             
            "unchecked_default" : [ "Availability", "Difficulty", "Cleansheets", 
                  "Saves", "ICT-Index", "Crosses", "Chances-Created", 
                  "Chances-Missed", "Target-Missed", "Clearance-Block", 
                  "Recoveries", "Tackles", "Tackled", 
                  "Key-Passes", "Winning-Goals", "Attempted-Passes", 
                  "Completed-Passes", "Penalties-Conceded", 
                  "Offside", "Fouls", "Dribbles"]
        }