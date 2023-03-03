from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str 
    date: date 
    isProject: bool 
    url: str 
    github: Optional[str] 
    
class User(SQLModel):
    username: str 
    email: str
    
class SuperUserCreate(User):
    password: str
    
class SuperUser(SuperUserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    
def create_tables(engine):
    SQLModel.metadata.create_all(bind=engine)
