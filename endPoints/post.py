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

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=list[Item])
def get_posts(db: Session = Depends(get_session)):
    return crud.get_allposts(db)


@router.get('/{post_id}', response_model=Item)
def get_post(post_id: int, db: Session = Depends(get_session)):
    return crud.get_item(db, post_id)


@router.post('/', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    crud.create_post(db, post)
    return post


@router.put('/{post_id}', response_model=Item)
def update_post(post_id: int, post: Post, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    crud.update_item(db, post_id, post)
    return post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    return crud.remove_item(db, post_id)
