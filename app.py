import os 
from dotenv import load_dotenv 
from pathlib import Path 
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, create_engine
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db.models import create_tables, Item, SuperUser, User
from db import crud, auth

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

def get_session():
    with Session(engine) as session:
        yield session
    
@app.on_event("startup")
def on_startup():
    create_tables(engine)

@app.get("/")
async def root():
    return {"message": "root page"}

@app.post('/posts/', response_model=Item)
def create_post(post: Item, db: Session = Depends(get_session),token: str = Depends(auth.oauth2_scheme)):
    crud.create_post(db, post)
    return post 

@app.get('/posts/', response_model=list[Item])
def get_posts(db: Session = Depends(get_session)):
    return crud.get_allposts(db) 

@app.delete('/post/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int, db: Session = Depends(get_session), token: str = Depends(auth.oauth2_scheme)): 
    return crud.remove_post(db, post_id)

@app.post('/users/', response_model=User)
def create_user(user: SuperUser, db: Session = Depends(get_session),token: str = Depends(auth.oauth2_scheme)):
    auth.create_user(db, user)
    return user 

@app.get('/users/', response_model=list[User])
def get_all_users(db: Session = Depends(get_session)):
    return crud.get_allusers(db) 

@app.get('/users/{username}', response_model=User)
def get_user(username:str, db: Session = Depends(get_session)):
    return crud.get_user(db, username) 

@app.post("/token", response_model=auth.Token)
def login(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    return auth.login_for_access_token(db, form_data)

@app.get('/current/', response_model=User)
def get_curruser(db: Session = Depends(get_session),token: str = Depends(auth.oauth2_scheme)):
    return auth.get_current_user(db, token) 

    



