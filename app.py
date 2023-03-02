from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from db.models import Base
from db.session import engine, get_db
import db.schemas as Schemas
from db import crud, auth


def create_tables():
    Base.metadata.create_all(bind=engine)

def start_app():
    create_tables()
    app = FastAPI()
    return app 

app = start_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "root page"}

@app.post('/posts/', response_model=Schemas.Item)
def create_post(post: Schemas.Item, db: Session = Depends(get_db),token: str = Depends(auth.oauth2_scheme)):
    crud.create_post(db, post)
    return post 

@app.get('/posts/', response_model=list[Schemas.Item])
def get_posts(db: Session = Depends(get_db)):
    return crud.get_allposts(db) 

@app.delete('/post/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int, db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return crud.remove_post(db, post_id)

@app.post('/users/', response_model=Schemas.User)
def create_user(user: Schemas.SuperUser, db: Session = Depends(get_db),token: str = Depends(auth.oauth2_scheme)):
    auth.create_user(db, user)
    return user 

@app.get('/users/', response_model=list[Schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_allusers(db) 

@app.get('/users/{username}', response_model=Schemas.User)
def get_user(username:str, db: Session = Depends(get_db)):
    return crud.get_user(db, username) 

@app.post("/token", response_model=auth.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return auth.login_for_access_token(db, form_data)

@app.get('/current/', response_model=Schemas.User)
def get_curruser(db: Session = Depends(get_db),token: str = Depends(auth.oauth2_scheme)):
    return auth.get_current_user(db, token) 

    



