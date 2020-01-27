
import json
from simulator import Simulator
from channels.click_bot import ClickBot
from channels.zara_bot import ZaraBot
from telethon import TelegramClient
from telethon import sync, events
import time

class Main():
    def __init__(self, config):
        self.simulator = Simulator()
        self.teleClient = TelegramClient(config['API_NAME'], config['API_ID'], config['API_HASH'])
        self.teleClient.start()

        ClickBot(self.teleClient, config['CLICK_CHANNEL']['click_bot'], self.simulator, config['API_NAME'])

        print('sleep 1h')
        time.sleep(3600)
        
    def __del__(self):
        print("Close connection")
        self.teleClient.disconnect()

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    Main(config)