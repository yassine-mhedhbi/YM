from fastapi import APIRouter
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlmodel import Session, create_engine
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db.models import create_tables, Item, Post, Project, SuperUser, User
from db import auth
import crud

from session import get_session
import logging
print(crud)
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
