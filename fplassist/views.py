# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:42:37 2017

@author: Ameen
"""
from django.shortcuts import render
from django.http import HttpResponse
from fplassist import generate_table
from django.http import JsonResponse
from fplassist import update_database

from rq import Queue
from worker import conn

import json

def fplassist(request):
    return render(request, 'fplassist.html')

def updatedb(request):
    with open('static/data/bgActive.json') as f:
        bg_active = json.loads(f.read())["bg_active"]
        if bg_active == 1:
            return HttpResponse("Database is updating in the background...")
        else:
            q = Queue(connection=conn)
            result = q.enqueue(update_database.update_database)
            return HttpResponse("Database update initiated: " + str(result))

def genTable(request):
    with open('static/data/bgActive.json') as f:
        bg_active = json.loads(f.read())["bg_active"]
        if bg_active == 1:
            return HttpResponse("Database is updating in the background...")
        else:
            return JsonResponse(generate_table.generate_table(), safe=False)

def update_table(request):
    with open('static/data/bgActive.json') as f:
        bg_active = json.loads(f.read())["bg_active"]
        if bg_active == 1:
            return HttpResponse("Database is updating in the background...")
        else:
            if request.method == 'POST':
                t_resp = generate_table.update_table(request.POST)
                return JsonResponse(t_resp, safe=False)