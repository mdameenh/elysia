# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:42:37 2017

@author: Ameen
"""

from django.shortcuts import render

def pathfinder(request):
    return render(request, 'pathfinder.html')