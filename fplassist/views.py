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


def fplassist(request):
    return render(request, 'fplassist.html')

def updatedb(request):
    status_key = update_database.update_database()
    if status_key == True:
        return HttpResponse("Database updated successfully")
    else:
        return HttpResponse("There was an error while updating database")

def genTable(request):
    return JsonResponse(generate_table.generate_table(), safe=False)

def updateTable(request):
    return HttpResponse(request.GET.get('cost', ''))