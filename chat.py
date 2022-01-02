from queue import Empty
import requests
import telepot
from threading import Thread
import json

class Chat:
    def __init__(self):
        self.token = "ENTER YOUR BOT KEY HERE"
        self.chat_id = {}
        self.bot = telepot.Bot(self.token)

        self.load_list()

        thread = Thread(target=self.start)
        thread.daemon = True
        thread.start()

    def save_list(self):
        with open('data.json', 'w') as fp:
            json.dump(self.chat_id, fp)

    def load_list(self):
        with open('data.json', 'r') as fp:
            data = json.load(fp)
            print("Loading data {}".format(data))
            self.chat_id = data

    def send_message(self,text):
        if self.chat_id is Empty:
            print("No chat id found")
        for chat_id in self.chat_id:
            if type(chat_id) is str:
                self.bot.sendPhoto(chat_id, open("temp.jpg", "rb"),text)

    
    def handle(self,msg):
        chat_id = msg['chat']['id']
        # message_id = msg['message_id']                  # I can get Id of incoming messages here 
        command = msg['text']

        if command == '/subscribe':
            if chat_id in self.chat_id:
                self.bot.sendMessage(chat_id, "You are already registered")
            else:
                self.chat_id[chat_id] = chat_id
                self.save_list()
                self.load_list()
                self.bot.sendMessage(chat_id, 'Successfully registered to message broker')
        elif command == '/unsubscribe':
            if str(chat_id) in self.chat_id:
                del self.chat_id[str(chat_id)]
                self.save_list()
                self.bot.sendMessage(chat_id, 'Successfully unregistered to message broker')
            else:
                self.bot.sendMessage(chat_id, "You are not registered")
        elif command == '/list':
            self.bot.sendMessage(chat_id, 'Registered users: ' + str(self.chat_id))
        elif command == '/start':
            self.bot.sendMessage(chat_id, 'Welcome to Motion Detector Bot, Here are the list of of command you can use: \n/subscribe \n/unsubscribe \n/list \n/start')
        else:
            self.bot.sendMessage(chat_id, 'Command not found')

    def start(self):
        self.bot.message_loop(self.handle, run_forever = 'Running ...')