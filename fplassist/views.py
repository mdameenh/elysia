# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:42:37 2017

@author: Ameen
"""
from django.shortcuts import render
from django.http import HttpResponse
from fplassist.generate_table import update_table
from django.http import JsonResponse
from fplassist import update_database
from fplassist.models import FPL_Config
from rq import Queue
from worker import conn
from fplassist.contexts import context

def fplassist(request):    
    return render(request, 'fplassist.html', context)

def updatedb(request):
    p = FPL_Config.objects.get(id=1)

    if p.bg_active == True:
        return HttpResponse("Database is updating in the background...")
    else:
        p.bg_active = True
        p.save()
        q = Queue(connection=conn)
        result = q.enqueue(update_database.update_database)
        return HttpResponse("Database update initiated: " + str(result))


def updatetable(request):
    p = FPL_Config.objects.get(id=1)

    if p.bg_active == True:
        return HttpResponse("Database is updating in the background...")
    else:
        if request.method == 'POST':
            t_resp = update_table(request.POST)
            return JsonResponse(t_resp, safe=False)