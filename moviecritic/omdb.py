# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 15:49:47 2017

@author: Ameen

Sample request : http://www.omdbapi.com/?t=Care+Bears:+Share+Bear+Shines&apikey=ab808c9c
"""


import json
from urllib.parse import urlencode 
from moviecritic.models import Movie_Details
from elysia.settings import BASE_DIR
import requests, os


API_KEY = "ab808c9c"

def run_omdb(key, wiki_file):
    movie_list = []
    wiki_data = None
    with open(os.path.join(BASE_DIR, wiki_file)) as f:
        wiki_data = json.load(f)
   
    for year, movies in wiki_data.items():
        for movie in movies:
            query = {'t': movie, 'apikey': key}
            url = 'http://www.omdbapi.com/?' + urlencode(query)
            print(url)
            movie_data = requests.get(url).json()
            if movie_data["Response"] == "True":
                movie_list.append(movie_data)
            else:
                print(movie_data)
                print("Error getting movie details!")
    with open(os.path.join(BASE_DIR, "moviecritic/movies.json"), 'w') as movie_file:
        json.dump(movie_list, movie_file, indent=4)

def update_movie_db(movie_file):
    with open(os.path.join(BASE_DIR, movie_file)) as movies_data_file:
        for movie in json.load(movies_data_file):
            print("Uploading %s" % (movie["Title"]))
            try:
                genre = [p.strip() for p in movie["Genre"].split(",")]
                director = [p.strip() for p in movie["Director"].split(",")]
                lang = [p.strip() for p in movie["Language"].split(",")]
                country = [p.strip() for p in movie["Country"].split(",")]
                prod = [p.strip() for p in movie["Production"].split(",")]
                
                for rating in movie["Ratings"]:
                    if rating["Source"] == "Internet Movie Database":
                        imdb = int(float(rating["Value"].split("/")[0]) * 10)
                    elif rating["Source"] == "Rotten Tomatoes":
                        rottentomatoes = int(rating["Value"].split("%")[0])
                    elif rating["Source"] == "Metacritic":
                        metacritic = int(rating["Value"].split("/")[0])
                if movie["BoxOffice"] != "N/A":
                    boxoffice = int(eval(movie["BoxOffice"].strip("$").replace(",", "")))
                else:
                    boxoffice = 0
            except KeyError:
                print("Problem with api data. Ignore and continue.")
                continue
            obj, created = Movie_Details.objects.get_or_create(name=movie["Title"],
                                                year=movie["Year"],
                                                defaults={'genre': genre,
                                                          'director': director,
                                                          'lang': lang,
                                                          'country': country,
                                                          'prod': prod,
                                                          'imdb': imdb,
                                                          'rottentomatoes': rottentomatoes,
                                                          'metacritic': metacritic,
                                                          'boxoffice': boxoffice})
        

def omdb():
    run_omdb(API_KEY, "moviecritic/data.json")
    update_movie_db("moviecritic/movies.json")

if __name__ == "__main__":
    omdb()