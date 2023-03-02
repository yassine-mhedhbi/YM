from pydantic import BaseModel
from datetime import date
from typing import Optional

class Item(BaseModel):
    id: Optional[int]
    title: Optional[str]
    date: Optional[date]
    isProject: Optional[bool]
    url: Optional[str]
    github: Optional[str]
    notebook: Optional[str]
    
    class Config:
        orm_mode = True

class User(BaseModel):
    username: str 
    email: str
    class Config:
        orm_mode = True
    
class SuperUser(User):
    id: int    
    password: str 


