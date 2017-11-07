from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import json, os
from moviecritic.omdb import omdb
from elysia.settings import BASE_DIR
from rq import Queue
from worker import conn
# Create your views here.

def updatedb(request):    
    q = Queue(connection=conn)
    result = q.enqueue(omdb, timeout=600)
    return HttpResponse("Database update initiated: " + str(result))    
    
def moviecritic(request):
    return  render(request, 'moviecritic.html')

def get_movie_details(request):
    with open(os.path.join(BASE_DIR, "moviecritic/movies.json")) as f:
        return JsonResponse(json.load(f), safe=False)
    