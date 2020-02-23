#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from telethon import TelegramClient
from telethon import sync, events
import time
import os
import sys


class Main:
    def __init__(self, config):
        print("[ " + config['API_NAME'] + " ] Connecting...")
        self.teleClient = TelegramClient(config['API_NAME'], config['API_ID'], config['API_HASH'])
        self.teleClient.start()
        print("[ " + config['API_NAME'] + " ] Connected")
        time.sleep(2)

    def __del__(self):
        print("Close connection")
        self.teleClient.disconnect()


if __name__ == "__main__":
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../config.json', 'r') as f:
        configs = json.load(f)
        Main(configs[int(sys.argv[1])])
