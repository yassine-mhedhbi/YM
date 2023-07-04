from fastapi import APIRouter
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlmodel import Session, create_engine
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db.models import create_tables, Create_Project, Project, SuperUser, User
from . import auth
from db import crud
from inspect import getmembers
from session import get_session
import logging
from typing import List

router = APIRouter(
    prefix="/projects",
    tags=["Project"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[Project])
def get_projects(db: Session = Depends(get_session)):
    return crud.get_allprojects(db)


@router.get('/{project_id}', response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_session)):
    return crud.get_project(db, project_id)


@router.post('/', response_model=Project)
def create_project(post: Create_Project, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    crud.create_project(db, post)
    return post


@router.put('/{project_id}', response_model=Project)
def update_project(project_id: int, post: Project, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    crud.update_project(db, project_id, post)
    return post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project(post_id: int, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    return crud.remove_project(db, post_id)
