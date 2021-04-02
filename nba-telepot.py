#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import subprocess
import telepot
import os
import urllib.request
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
api_base_url="http://data.nba.net/10s"
def get_scoreboard():
    index=requests.get(api_base_url+"/prod/v1/today.json").json()
    scoreboard_url=index["links"]["todayScoreboard"]
    return scoreboard_url
def get_point_today(team_id):
    scoreboard=requests.get(api_base_url+get_scoreboard()).json()
    output=""
    for game in scoreboard["games"]:
        output+=game["vTeam"]["triCode"]+":"+game["vTeam"]["score"]
        output+=" / "
        output+=game["hTeam"]["triCode"]+":"+game["hTeam"]["score"]
        output+=" / "
        output+=str(game["period"]["current"])+" "+str(game["clock"])+"\n"
    return output
def get_point_by_date(date):
    scoreboard=requests.get("http://data.nba.net/prod/v1/"+date+"/scoreboard.json").json()
    output=""
    for game in scoreboard["games"]:
        output+=game["vTeam"]["triCode"]+":"+game["vTeam"]["score"]
        output+=" / "
        output+=game["hTeam"]["triCode"]+":"+game["hTeam"]["score"]
        output+=" / "
        output+=str(game["period"]["current"])+" "+str(game["clock"])+"\n"
    return output
def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        print ("Command from client : %s  " %command)
        with urllib.request.urlopen("http://data.nba.net/10s/prod/v1/today.json") as url:
            backl = json.loads(url.read().decode())
    #nbasearch
        if command == '/start':
            bot.sendMessage(chat_id,'請輸入要查詢之日期(格式如20200928)，如要查詢目前請輸入today')
        elif command == 'today':
            data=get_point_today(command)
            bot.sendMessage(chat_id, data)
            #bot.sendMessage(chat_id, "success")
            print ("Sent!")
        else:
            data=get_point_by_date(command)
            bot.sendMessage(chat_id, data)
            #bot.sendMessage(chat_id, "success")
            print ("Sent!")
            
    #end youtube search



#api credentials
api = open('api.txt','r')
api_cont = api.read().strip()
bot = telepot.Bot(api_cont)
bot.message_loop(handle)
print ('[+] Server is Listenining [+]')
print ('[=] Type Command from Telegram [=]')

while 1:
        time.sleep(10)
