from typing import Union
from pydantic import BaseModel

class Victim(BaseModel):
    name: str
    UUID: str
    IP: Union[str, None] = None
    OS: Union[str, None] = None