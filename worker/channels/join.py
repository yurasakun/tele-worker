from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.messages import DeleteChatUserRequest
import urllib.request
import re
import time
from datetime import datetime


class MsgCheck():
    def __init__(self, teleClient, channel, browser, name):
        self.name = name
        self.simulator = browser
        self.teleClient = teleClient
        self.currentChannel = channel
        self.currentChat = self.getChannel(self.currentChannel)
        self.noAds = 0
        # self.checkWidthraw(self.currentChat)
        while self.noAds != 2:
            self.messageCheck(self.currentChat)
        self.checkWidthraw(self.currentChat)

    def checkWidthraw(self, chat):
        self.teleClient.send_message("@"+self.currentChat.username, "💵 Withdraw")
        time.sleep(5)
        msg = self.teleClient.get_messages(chat, limit=1)
        widthraw_data = re.findall("\d+\.\d+", msg[0].message)
        try:
            print("[ " + self.name + " ] " + "My balance {} DOGE".format(widthraw_data[0]))
        except:
            print("[ " + self.name + " ] " + "My balance {0} DOGE")
        if len(widthraw_data) == 1:
            self.teleClient.send_message("@"+self.currentChat.username, self.currentChannel['wallet'])
            time.sleep(5)
            self.teleClient.send_message("@"+self.currentChat.username, widthraw_data[0])
            time.sleep(5)
            self.teleClient.send_message("@"+self.currentChat.username, "✅ Confirm")

    def messageCheck(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        now = datetime.now()

        print("[ " + self.name + " ] " + "Get new task from " + self.currentChat.firs_name + " at ({})".format(
            now.strftime("%H:%M:%S")))

        if any(ele in msg[0].message for ele in ['no new ads']):
            self.noAds = self.noAds + 1

        self.teleClient.send_message("@"+self.currentChat.username, "/bots")
        time.sleep(5)
        self.getReward(chat)

    def getReward(self, chat):
        try:
            msg = self.teleClient.get_messages(chat, limit=1)
            time.sleep(5)
            channel_msg = msg[0].reply_markup.rows[0].buttons[0].url
            message_id = msg[0].id
            button_data = msg[0].reply_markup.rows[1].buttons[1].data

            print("[ " + self.name + " ] " + f'URL @{channel_msg}')
            channel_name = self.returnName(channel_msg)

            print("[ " + self.name + " ] " + f'Messaging @{channel_name}...')
            time.sleep(1)
            try:
                msg_channel = self.teleClient.send_message(channel_name, '/start')
                time.sleep(5)
                msg_get = self.teleClient.get_messages(channel_name, limit=1)
                msg_text = msg_get[0].raw_text
                if "/start" in msg_text and len(msg_text)==6:
                    self.teleClient(GetBotCallbackAnswerRequest(
                    chat,
                    message_id,
                    data=button_data
                    ))
                    print("[ " + self.name + " ] " + "Skiping task.....")
                else:
                    message_channel_id = msg_get[0].id
                    self.teleClient.forward_messages("@"+self.currentChat.username, message_channel_id, channel_name)
                    print("[ " + self.name + " ] " + "Forward message send good good!")
                    
                    

                




            except:
                self.teleClient(GetBotCallbackAnswerRequest(
                    chat,
                    message_id,
                    data=button_data
                ))
        except:
            print(
                "[ " + self.name + " ] " + "no new ads available form for MsgBot " + self.currentChat.firstname + " (" + str(
                    self.noAds) + ")")

    def GetChatsId(self, channel):
        dlgs = self.teleClient.get_dialogs()
        for dlg in dlgs:
            if dlg.title == channel:
                return dlg.id


    def returnName(self, link):
        link = link[link.find("/") + 2:]
        if '?' in link:
            link = link[link.find("/") + 1: link.find("?")]
        else:
            link = link[link.find("/") + 1:]
        return link

    def getChannel(self, channel):
        dlgs = self.teleClient.get_entity("@"+channel['id'])
        return dlgs
