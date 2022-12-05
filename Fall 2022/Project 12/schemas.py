from typing import List, Union, Sequence, Optional
from pydantic import BaseModel


class Title(BaseModel):
    title: str
    premiered: str
    runtime: str
    class Config:
        orm_mode: True




