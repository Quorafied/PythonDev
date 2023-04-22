import pydirectinput as io
import time
import pyperclip
# from main import client
import requests
import json

io.PAUSE = 0.07

class UserInterface():
    def __init__(self):
        self.running = False
        self.shouldStop = False
        self.bot_spam = True
        self.bot_channel = False
        self.allow = False
        self.targetChannelId = 690924498903498763
        self.botChannelId = 1098336491350011984

        self.botId = 861370829253509133
        self.dankId = 270904126974590976
        self.dynoId = 155149108183695360
        self.meeId = 159985870458322944
        self.ownId = 1058522888975691836
        self.botIds = [self.botId, self.dankId, self.dynoId, self.meeId, self.ownId]

        self.userToken = 'MTA1ODUyMjg4ODk3NTY5MTgzNg.GWF4Yz.mYo14ymuociw45ZMKPDuX2hUgKnUtszXAzjtBQ'

   
    def checkAuthor(self, id):
        print(f"id given: {id}")
        print(f"botIds: {self.botIds}")
        if int(id) not in self.botIds:
            self.allow = True
            print("allowed on")
        else: 
            self.allow = False
            print("allowed off")
        print(f"self.allow: {self.allow}")

    def check_forNewMessage(self):
        message = ws.retrieve_messages(self.targetChannelId)
        if message is False:
            return False
        
        time.sleep(0.2)
        self.checkAuthor(message.authorId)
        if self.allow is False:
            return False
        
        print(f"messageAuthor: {message.authorId}, messageText: {message.content}")
        if message.content[:2] != "q.":
            print("Message does is not a command")
            return False
    
        return message

    def send_messageToBot(self, message):
        if message is False:
            return "can't do that."
        
        ws.sendMsg_toBot(self.botChannelId, message.content)

ui = UserInterface()
class Message():
    def __init__(self, txt="", authorid=0):
        self.content = txt
        self.authorId = authorid

class WebScraper():
    def __init__(self):
        self.toSend_Message = ""
        self.wait = False
    def check_for_previousMessage(self, message):
        if message.content == self.toSend_Message:
            return False
        else: return True

    def check_statusCode(self, response):
        if response.status_code != 200:
            print(f"Failed to send message: {response.status_code} - {response.text}")
        else:
            print("Message sent succesfully")

    def retrieve_messages(self, channelid):
        if self.wait == True:
            return False
        
        headers = {
            'Authorization': f'{ui.userToken}'
        }

        response = requests.get(f"https://discord.com/api/v9/channels/{str(channelid)}/messages", headers=headers)

        jsonn = json.loads(response.text)
        message = Message(jsonn[0]["content"], jsonn[0]['author']['id'])

        self.check_statusCode(response)
        
        if self.check_for_previousMessage(message):
            return message
        else: 
            print("Same message \n\n")
            return False
    

    def sendMsg_toBot(self, channelid, content):
        self.wait = True
        headers = {
            "Authorization": f"{ui.userToken}",
            "Content-Type": "application/json"
        }

        payload = {"content": content}
        response = requests.post(f"https://discord.com/api/v9/channels/{str(channelid)}/messages", headers=headers, json=payload)

        self.check_statusCode(response)

    def send_response(self, channelid):
        headers = {
            "Authorization": f"{ui.userToken}",
            "Content-Type": "application/json"
        }

        payload = {"content": self.toSend_Message}
        response = requests.post(f"https://discord.com/api/v9/channels/{str(channelid)}/messages", headers=headers, json=payload)

        self.check_statusCode(response)
        time.sleep(1)
        self.wait = False
        

ws = WebScraper()
