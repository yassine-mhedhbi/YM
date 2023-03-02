from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String)
    date = Column(Date)
    isProject = Column(Boolean)
    url = Column(String, nullable=True)
    github = Column(String, nullable=True)
    notebook = Column(String, nullable=True)
    
    
class SuperUser(Base):
    __tablename__ = 'superusers'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
