#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

import urllib.request
import re
import time
from datetime import datetime

class ZaraBot():
    def __init__(self, teleClient, channel, browser):
        self.teleClient = teleClient
        self.simulator = browser
        self.currentChannel = channel
        self.currentChat = self.getChannel(self.currentChannel)
        self.noAds = 0
        while self.noAds != 1:
            self.messageCheck(self.currentChat)
 
    def messageCheck(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        print("="*15)
        now = datetime.now()
        print("Get new task from " + self.currentChat.name + " ({})".format(now.strftime("%H:%M:%S")))

        if any(ele in msg[0].message for ele in ['Пока нет постов']):
            self.noAds = self.noAds +1

            print("No ads aviable from "  + self.currentChat.name  + " (" + str(self.noAds) + ")")

            self.teleClient.send_message(self.currentChat.name, "👀 Просмотреть")
            time.sleep(10)
            self.getReward(chat)
        else:
            self.teleClient.send_message(self.currentChat.name, "👀 Просмотреть")
            time.sleep(10)
            self.getReward(chat)

    def getReward(self, chat):
        check = 0
        msg = ""
        while any(ele in msg for ele in ['no new ads']) and check != 3:
            msgs = self.teleClient.get_messages(chat, limit=1)
            msg = msgs[0].message
            print('Check reward ' + str(check))
            time.sleep(10)
        msgs = self.teleClient.get_messages(chat, limit=1)
        print(msgs[0].message)

    def getChannel(self, channel):
        dlgs = self.teleClient.get_dialogs()
        for dlg in dlgs:
            if dlg.title == channel['name']:
                return dlg