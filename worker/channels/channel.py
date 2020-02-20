from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.messages import DeleteChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest
import urllib.request
import re
import time
from datetime import datetime


class JoinChannel():
    def __init__(self, teleClient, channel, browser, name):
        self.name = name
        self.simulator = browser
        self.teleClient = teleClient
        self.currentChannel = channel
        self.currentChat = self.getChannel(self.currentChannel)
        self.Ads = 0
        # self.checkWidthraw(self.currentChat)
        while self.Ads != 10:
            self.messageCheck(self.currentChat)
        # self.checkWidthraw(self.currentChat)

    def messageCheck(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        now = datetime.now()

        print("[ " + self.name + " ] " + "Get new task from " + self.currentChat.name + " at ({})".format(
            now.strftime("%H:%M:%S")))

        self.teleClient.send_message(self.currentChat.name, "/join")
        time.sleep(5)
        self.getReward(chat)
        self.Ads = self.Ads + 1
        print("proideno " + str(self.Ads))

        def getReward(self, chat):
        try:
            msg = self.teleClient.get_messages(chat, limit=1)
            time.sleep(5)
            channel_msg = msg[0].reply_markup.rows[0].buttons[0].url
            message_id = msg[0].id
            button_data = msg[0].reply_markup.rows[0].buttons[1].data

            button_data_skip = msg[0].reply_markup.rows[1].buttons[1].data

            channel_name = self.returnName(channel_msg)
            print("[ " + self.name + " ] " + f'Join @{channel_name}...')
            time.sleep(1)
            try:
                self.teleClient(JoinChannelRequest("@" + channel_name))
                print("[ " + self.name + " ] " + "Join CHANNEL!")

                self.teleClient(GetBotCallbackAnswerRequest(
                    chat,
                    message_id,
                    data=button_data
                ))
                self.CheckJoin(chat)

            except:
                self.teleClient(GetBotCallbackAnswerRequest(
                    chat,
                    message_id,
                    data=button_data_skip
                ))
                print("[ " + self.name + " ] " + "Skiping Task")
        except:
            print(
                "[ " + self.name + " ] " + "Erorr" + self.currentChat.name + " (" + str(
                    self.Ads) + ")")

    def CheckJoin(self, chat):
        msg = self.teleClient.get_messages(chat, limit=1)
        time.sleep(5)
        if "We cannot find you in the group" in msg[0].message:
            self.teleClient.send_message(self.currentChat.name, "/join")
            msg = self.teleClient.get_messages(chat, limit=1)
            time.sleep(5)
            message_id = msg[0].id
            button_data_skip = msg[0].reply_markup.rows[1].buttons[1].data
            self.teleClient(GetBotCallbackAnswerRequest(
                chat,
                message_id,
                data=button_data_skip
            ))
            print("[ " + self.name + " ] " + "skiping task...")
        else:
            print("[ " + self.name + " ] " + "Clicks the joined")

    def returnName(self, link):
        link = link[link.find("/") + 2:]
        if '?' in link:
            link = link[link.find("/") + 1: link.find("?")]
        else:
            link = link[link.find("/") + 1:]
        return link

    def getChannel(self, channel):
        dlgs = self.teleClient.get_dialogs()

        for dlg in dlgs:
            if dlg.title == channel['name']:
                return dlg
