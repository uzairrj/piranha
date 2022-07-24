from sqlite3 import Timestamp
from typing import Union
from pydantic import BaseModel

class Keylogs(BaseModel):
    timeStamp: Timestamp
    data: str
    UUID: str
    img: Union[str, None] = None
    