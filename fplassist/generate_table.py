# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 00:32:54 2017

@author: Ameen
"""
import os
from urllib import parse
import psycopg2

def generate_table():
    database = "db.sqlite3"
    print(database)
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
    cur.execute("SELECT * FROM players")
    player_list = []
    rows = cur.fetchall()
    rows = sorted(rows, key=lambda x : x[5], reverse=True)
    
    for _ in range(50):
        i = rows[_]
        player_list.append([i[0], i[1], i[2]/10, i[30], i[5],
        i[7], i[11], i[12], i[14], i[9], i[16], i[18],
        i[19], i[23], i[24], i[26], i[27]])

    return player_list