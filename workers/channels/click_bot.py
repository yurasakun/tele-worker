#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.channels import JoinChannelRequest
import urllib.request
import re
import time
from datetime import datetime


class ClickBot:
    def __init__(self, teleClient, channel, browser, name):
        self.name = name
        self.teleClient = teleClient
        self.simulator = browser
        self.currentChannel = channel
        self.currentChat = self.getChannel(self.currentChannel)
        self.noAds = 0
        self.checkWidthraw(self.currentChat)
        while self.noAds <= 5:
            try:
                self.messageCheck(self.currentChat)
            except: 
                pass

        self.noAds = 0

        if self.currentChannel["subscribe"]:
            while self.noAds <= 3:
                try:
                    self.joinChats(self.currentChat)
                except:
                    pass

        self.checkWidthraw(self.currentChat)

    def joinChats(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        time.sleep(3)
        self.teleClient.send_message(self.currentChat.id, "📣 Join chats")
        time.sleep(5)
 
        jMsg = self.teleClient.get_messages(chat, limit=1)

        if any(ele in jMsg[0].message for ele in ['no new ads']):
            self.noAds = self.noAds +1
            print("[ "+self.name +" ] " +"No new channel aviable from "  + self.currentChat.name  + " (" + str(self.noAds) + ")")
        
        else:
            channel_to_join = jMsg[0].reply_markup.rows[0].buttons[0].url.split("/")[-1]
            verity_btn = jMsg[0].reply_markup.rows[0].buttons[1].data
            skip_data = jMsg[0].reply_markup.rows[1].buttons[1].data
            message_id = jMsg[0].id

            if "We cannot find you in the group" in msg[0].message:
                print("skip")
                print("[ "+self.name +" ] " + "Skip " + str(channel_to_join))
            
                self.teleClient(GetBotCallbackAnswerRequest(
                    chat,
                    message_id,
                    data=skip_data
                ))
            else:
                try:
                    print("[ "+self.name +" ] " + "Join new channel \"" + str(channel_to_join) + "\"")
                    self.teleClient(JoinChannelRequest(channel_to_join))
                    time.sleep(5)
                    self.teleClient(GetBotCallbackAnswerRequest(
                        chat,
                        message_id,
                        data=verity_btn
                    ))
                except:
                    print("[ "+self.name +" ] " + "Error when try to join \"" + str(channel_to_join) + "\"")
                    self.noAds = self.noAds +1
                    self.teleClient(GetBotCallbackAnswerRequest(
                        chat,
                        message_id,
                        data=skip_data
                    ))

    def checkWidthraw(self, chat):
        self.teleClient.send_message(self.currentChat.id, "💵 Withdraw")
        time.sleep(5)
        msg = self.teleClient.get_messages(chat, limit=1)

        try:
            widthraw_data = re.findall("\d+\.\d+", msg[0].message)
            print("[ "+self.name +" ] " + "My balance {} ZEC".format(widthraw_data[0]))

            if len(widthraw_data) == 1:
                self.teleClient.send_message(self.currentChat.id, self.currentChannel['wallet'])
                time.sleep(5)
                self.teleClient.send_message(self.currentChat.id, widthraw_data[0])
                time.sleep(5)
                self.teleClient.send_message(self.currentChat.id, "✅ Confirm")

        except:
            print("[ "+self.name +" ] Cant Widthraw")
            time.sleep(5)
            self.teleClient.send_message(self.currentChat.id, "❌ Cancel")
            

    def messageCheck(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        now = datetime.now()

        if any(ele in msg[0].message for ele in ['seconds']):
            sleepTime = int(re.search(r'\d+', msg[0].message).group())
            print("[ "+self.name +" ] " + "Find reward!! Wait " + str(sleepTime) + " seconds.")
            time.sleep(sleepTime + 5)
            try:
                m = self.teleClient.get_messages(chat, limit=2)
                print("[ "+self.name +" ] " + "Get " + re.findall("\d+\.\d+", m[1].message)[0] + " ZEC")
                print('='*30)
            except:
                print("[ "+self.name +" ] Cant get reward amount")

        print("[ "+self.name +" ] " +"Get new task from " + self.currentChat.name + " at ({})".format(now.strftime("%H:%M:%S")))

        if any(ele in msg[0].message for ele in ['no new ads']):
            self.noAds = self.noAds +1
            print("[ "+self.name +" ] " +"No ads aviable from "  + self.currentChat.name  + " (" + str(self.noAds) + ")")

        self.teleClient.send_message(self.currentChat.id, "/visit")
        time.sleep(7)
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
            self.noAds = self.noAds +1
            return None


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
        dlgs = self.teleClient.get_dialogs()

        for dlg in dlgs:
            if dlg.entity.username == channel['id']:
                return dlg
