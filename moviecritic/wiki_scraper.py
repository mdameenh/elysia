# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 00:34:35 2017

@author: Ameen
"""

import lxml.html as ht
import requests
from json import dump

def runScraper():
    movie_list = {}
    for i in range(7):
        print("Movies #201%d" % i)
        movie_list["201%d" % i] = []
        link = "https://en.wikipedia.org/wiki/201%d_in_film" % (i)
        page = requests.get(link)
        wikitree = ht.fromstring(page.content)
    
        for table in wikitree.find_class("wikitable"):
            movieTable = [key for key in table.cssselect('th') if key.text_content() == 'Opening']
            if len(movieTable) == 0:
                continue
            for movie in table.cssselect('i'):
                movie_list["201%d" % i].append(movie.text_content().strip())
    
    with open('data.json', 'w') as data_file:
        dump(movie_list, data_file, indent=4)    

if __name__ == "__main__":
    runScraper()