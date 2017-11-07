from django.http import JsonResponse
from django.shortcuts import render
import json, os
from moviecritic.omdb import omdb
from elysia.settings import BASE_DIR

# Create your views here.

def updatedb(request):    
    omdb()
    with open(os.path.join(BASE_DIR, "moviecritic/movies.json")) as f:
        return JsonResponse(json.load(f), safe=False)
    
    
def moviecritic(request):
    return  render(request, 'moviecritic.html')