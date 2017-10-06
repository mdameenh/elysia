# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 00:32:54 2017

@author: Ameen
"""
import sqlite3

def generate_table():
    database = "db.sqlite3"
    print(database)
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Exception as e:
        print(e)

    cur = conn.cursor()
    cur.execute("SELECT * FROM players")
    player_list = []
    rows = cur.fetchall()

    for i in rows:
        player_list.append([i[0], i[1], i[2]/10, i[30], i[5],
        i[7], i[11], i[12], i[14], i[9], i[16], i[18],
        i[19], i[23], i[24], i[26], i[27]])

    return player_list