#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from simulator import Simulator
from channels.click_bot import ClickBot
from telethon import TelegramClient
from telethon import sync, events
import time
import os
import sys


class Main:
    def __init__(self, config):
        self.simulator = Simulator()
        self.teleClient = TelegramClient(config['API_NAME'], config['API_ID'], config['API_HASH'])
        self.teleClient.start()

        ClickBot(self.teleClient, config['CLICK_CHANNEL']['click_bot'], self.simulator, config['API_NAME'])
        
    def __del__(self):
        print("Close connection")
        self.teleClient.disconnect()


if __name__ == "__main__":
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../config.json', 'r') as f:
        configs = json.load(f)
        Main(configs[int(sys.argv[1])])
