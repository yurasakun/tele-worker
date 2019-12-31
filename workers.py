#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

os.system('mkdir workers')

def createWorker(worker):
    w_path = 'workers/w_' + worker['API_NAME']
    os.system('mkdir ' + w_path)
    os.system('cp -r worker/* ' + w_path)
    with open(w_path + '/config.json', 'w') as outfile:
        json.dump(worker, outfile)
        
with open('config.json', 'r') as f:
    workers = json.load(f)
    for worker in workers:
        createWorker(worker)
   