from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field


class Create_Project(SQLModel):
    title: str
    subtitle: str
    description: str
    date: date
    github: str
    url: Optional[str]
    post: Optional[str]
    img_path: str


class Project(Create_Project, table=True):
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
