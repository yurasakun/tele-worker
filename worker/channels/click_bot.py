#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

import urllib.request
import re
import time
from datetime import datetime


class ClickBot():
    def __init__(self, teleClient, channel, browser, name):
        self.name = name
        self.teleClient = teleClient
        self.simulator = browser
        self.currentChannel = channel
        self.currentChat = self.getChannel(self.currentChannel)
        self.noAds = 0
        self.checkWidthraw(self.currentChat)
        while self.noAds != 2:
            self.messageCheck(self.currentChat)
        self.checkWidthraw(self.currentChat)

    def checkWidthraw(self, chat):
        self.teleClient.send_message(self.currentChat.name, "💵 Withdraw")
        time.sleep(5)
        msg = self.teleClient.get_messages(chat, limit=1)
        widthraw_data = re.findall("\d+\.\d+", msg[0].message)
        try:
            print("[ " + self.name + " ] " + "My balance {} DOGE".format(widthraw_data[0]))
        except:
            print("[ " + self.name + " ] " + "My balance {0} DOGE")
        if len(widthraw_data) == 1:
            self.teleClient.send_message(self.currentChat.name, self.currentChannel['wallet'])
            time.sleep(5)
            self.teleClient.send_message(self.currentChat.name, widthraw_data[0])
            time.sleep(5)
            self.teleClient.send_message(self.currentChat.name, "✅ Confirm")
 

    def messageCheck(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        now = datetime.now()

        if any(ele in msg[0].message for ele in ['seconds']):
            sleepTime = int(re.search(r'\d+', msg[0].message).group())
            print("[ "+self.name +" ] " + "Find reward!! Wait " + str(sleepTime) + " seconds.")
            time.sleep(sleepTime + 1)
            print('='*30)

        print("[ "+self.name +" ] " +"Get new task from " + self.currentChat.first_name + " at ({})".format(now.strftime("%H:%M:%S")))

        if any(ele in msg[0].message for ele in ['no new ads']):
            self.noAds = self.noAds +1
            print("[ "+self.name +" ] " +"No ads aviable from "  + self.currentChat.first_name  + " (" + str(self.noAds) + ")")

        self.teleClient.send_message("@"+self.currentChat.username, "/visit")
        time.sleep(5)
        self.getReward(chat)


    def getReward(self, chat):
        try:
            msg = self.teleClient.get_messages(chat, limit=1)
            button_data = msg[0].reply_markup.rows[1].buttons[1].data
            message_id = msg[0].id
            url = msg[0].reply_markup.rows[0].buttons[0].url

            if self.checkUrl(url ,message_id, button_data, chat):
                print("[ "+self.name +" ] " +"Opening url: " + url)
                self.simulator.get_html(url)
            else:
                print("[ "+self.name +" ] " +'No reward')
        except:
            print("[ "+self.name +" ] " +"Cant find ads url")



    def checkUrl(self, url, message_id, button_data, chat):
        try:
            openUrl = urllib.request.urlopen(url)
            myBytes = openUrl.read()
            pageStr = myBytes.decode("utf8")
        except:
            return False

        if re.search(r'\breCAPTCHA\b', pageStr):
            time.sleep(5)
            print("[ "+self.name +" ] " +"Skiping task...")
            self.teleClient(GetBotCallbackAnswerRequest(
                        chat,
                        message_id,
                        data=button_data
                    ))
            return False
        else:
            return True


    def getChannel(self, channel):
        dlgs = self.teleClient.get_entity("@"+channel['id'])
        return dlgs

