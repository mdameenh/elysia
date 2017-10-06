# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:42:37 2017

@author: Ameen
"""

from django.http import HttpResponse

def index(request):
    return HttpResponse("There is nothing here. Try /fplassist")
