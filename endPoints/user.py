from fastapi import APIRouter
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Depends, status
from sqlmodel import Session, create_engine
from db.models import create_tables, SuperUser, User
from . import auth
from db import crud
from inspect import getmembers
from pprint import pprint
from session import get_session
import logging

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: SuperUser, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    auth.create_user(db, user)
    return user


@router.get('/', response_model=list[User])
def get_all_users(db: Session = Depends(get_session)):
    return crud.get_allusers(db)


@router.get('/{username}', response_model=User)
def get_user(username: str, db: Session = Depends(get_session)):
    return crud.get_user(db, username)
