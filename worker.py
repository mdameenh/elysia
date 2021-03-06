# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 00:41:41 2017

@author: Ameen
"""

import os

import redis, django
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    django.setup()
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
