import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlmodel import Session, create_engine
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db.models import create_tables, Item, Post, Project, SuperUser, User
from db import auth
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging
from session import get_session
from fastapi import APIRouter
# from endPoints import user, project, post


load_dotenv(dotenv_path=Path('.') / '.env')

engine = create_engine(os.getenv('DATABASE_URI'))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.middleware("http")
async def add_range(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Total-Count'] = '30'
    response.headers['Access-Control-Expose-Headers'] = 'X-Total-Count'
    return response


@app.on_event("startup")
def on_startup():
    create_tables(engine)


@app.get("/")
async def root():
    return {"message": "root page"}


@app.post("/token", response_model=auth.Token)
def login(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    return auth.login_for_access_token(db, form_data)


@app.get('/current/', response_model=User)
def get_curruser(db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)):
    return auth.get_current_user(db, token)


# app.include_router(api_router)
