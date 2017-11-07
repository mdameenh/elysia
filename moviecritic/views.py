from django.http import JsonResponse
from django.shortcuts import render
import json
from moviecritic.omdb import omdb

# Create your views here.

def updatedb(request):    
    omdb()
    with open("moviecritic\movies.json") as f:
        return JsonResponse(json.load(f), safe=False)
    
    
def moviecritic(request):
    return  render(request, 'moviecritic.html')