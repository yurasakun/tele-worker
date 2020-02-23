#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, subprocess, time, signal, time
import datetime
import time
import subprocess
import glob

dir_path = os.path.dirname(os.path.realpath(__file__))


while True:
	now_time = time.time()
	last = 0
	update_time_h = 12

	try:
		with open("lastboot", "r") as inp:
			last = int(inp.readlines()[0])

		if (now_time - last > (3600 * update_time_h)) is False:
			sleep_time = int((3600 * update_time_h) - (now_time - last))
			print("wait for new circle: " + str(datetime.timedelta(seconds=sleep_time)))

			time.sleep(sleep_time)
	except:
		print("No last boot data")

	with open("lastboot", "w") as lb:
			lb.writelines(str(int(time.time())))

	for w in range(len(glob.glob('workers/*.session'))):
		worker = subprocess.call(["python3",  dir_path + "/workers/main.py", str(w)], cwd="workers")


