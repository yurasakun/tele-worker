#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def createContainer(worker):
    cmd = """sudo docker run -d --name w_{0} --restart always \
    -v /home/botfarm/tele-worker/workers/w_{0}:/usr/src/app \
     tele-worker:latest
    """.format(worker['API_NAME'])

    os.system(cmd)
with open('config.json', 'r') as f:
    workers = json.load(f)
    for worker in workers:
        createContainer(worker)