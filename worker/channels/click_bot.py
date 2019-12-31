#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

import urllib.request
import re
import time
from datetime import datetime


class ClickBot():
    def __init__(self, teleClient, channel, browser):
        self.teleClient = teleClient
        self.simulator = browser
        self.currentChannel = channel
        self.currentChat = self.getChannel(self.currentChannel)
        self.noAds = 0
        while self.noAds != 2:
            self.messageCheck(self.currentChat)
 
    def messageCheck(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        print("="*15)
        now = datetime.now()
        print("Get new task from " + self.currentChat.name + " ({})".format(now.strftime("%H:%M:%S")))

        if any(ele in msg[0].message for ele in ['no new ads']):
            self.noAds = self.noAds +1

            print("No ads aviable from "  + self.currentChat.name  + " (" + str(self.noAds) + ")")

            self.teleClient.send_message(self.currentChat.name, "/visit")
            time.sleep(5)
        else:
            self.teleClient.send_message(self.currentChat.name, "/visit")
            time.sleep(5)
            self.getReward(chat)

    def getReward(self, chat):
            msg = self.teleClient.get_messages(chat, limit=1)
            button_data = msg[0].reply_markup.rows[1].buttons[1].data
            message_id = msg[0].id
            url = msg[0].reply_markup.rows[0].buttons[0].url
            print(url)

            if self.checkUrl(url ,message_id, button_data, chat):
                self.simulator.get_html(url)

                print("Open url")
                time.sleep(3)
                msg = self.teleClient.get_messages(chat, limit=1)

                if any(ele in msg[0].message for ele in ['seconds']):
                    sleepTime = int(re.search(r'\d+', msg[0].message).group())
                    print("Find reward " + str(sleepTime))
                    time.sleep(sleepTime + 1)
            else:
                print('No reward')

    def checkUrl(self, url, message_id, button_data, chat):
        try:
            openUrl = urllib.request.urlopen(url)
            myBytes = openUrl.read()
            pageStr = myBytes.decode("utf8")
        except:
            return False

        if re.search(r'\breCAPTCHA\b', pageStr):
            time.sleep(5)
            print("Capcha!")
            self.teleClient(GetBotCallbackAnswerRequest(
                        chat,
                        message_id,
                        data=button_data
                    ))
            return False
        else:
            return True
        
    # def nextDialog(self):
    #     selected = self.channels.index(self.currentChannel)
    #     nextChannel = 0

    #     if selected == len(self.channels) -1:
    #         nextChannel = 0
    #     else:
    #         nextChannel = selected + 1
        
    #     return self.channels[nextChannel]

    def getChannel(self, channel):
        dlgs = self.teleClient.get_dialogs()

        for dlg in dlgs:
            if dlg.title == channel['name']:
                return dlg