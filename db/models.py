import os 
from dotenv import load_dotenv 
from pathlib import Path 
from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, create_engine
 
load_dotenv(dotenv_path=Path('.') / '.env')

engine = create_engine(os.getenv('DATABASE_URI'))

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str 
    date: date 
    isProject: bool 
    url: str 
    github: Optional[str] 
    
    
class SuperUser(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str 
    email: str 
    password: str
 
    
def create_tables():
    SQLModel.metadata.create_all(bind=engine)
