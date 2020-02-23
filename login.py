#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json', 'r') as f:
    configs = json.load(f)
    for w in range(len(configs)):
        worker = subprocess.call(["python3",  dir_path + "/workers/login.py", str(w)], cwd="workers")