from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class Post(SQLModel):
    title: str
    date: date
    isProject: bool = False
    url: str
    url_img: str


class Project(Post):
    github: Optional[str] = Field(default=None)
    isProject = True


class Item(Project, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class User(SQLModel):
    id: Optional[int]
    username: str
    email: str


class SuperUserCreate(User):
    password: str


class SuperUser(SuperUserCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


def create_tables(engine):
    SQLModel.metadata.create_all(bind=engine)
