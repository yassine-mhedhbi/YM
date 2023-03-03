from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas 

def get_user(db: Session, username: str):
    return db.query(models.SuperUser).filter(models.SuperUser.username == username).first()

def get_allusers(db: Session):
    return db.query(models.SuperUser).all()

def create_user(db: Session, user: schemas.SuperUser, pwd_context:CryptContext):
    user = models.SuperUser(**user.dict())
    user.password = pwd_context.hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_post(db: Session, post_id: int):
    db.query(models.Item).filter(models.Item.id == post_id).first()
    
def get_allposts(db: Session):
    return db.query(models.Item).all()

def create_post(db: Session, post: schemas.Item):
    post = models.Item(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post 

def remove_post(db: Session, post_id: int):
    db.query(models.Item).filter(models.Item.id == post_id).delete()
    db.commit()
    return  