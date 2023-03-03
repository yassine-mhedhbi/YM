from sqlmodel import Session, select
from passlib.context import CryptContext
from .models import Item, SuperUserCreate, SuperUser

def get_user(db: Session, username: str):
    return db.exec(select(SuperUser).where(SuperUser.username == username)).one()

def get_allusers(db: Session):
    return db.exec(select(SuperUser)).all()

def create_user(db: Session, user: SuperUserCreate, pwd_context:CryptContext):
    user.password = pwd_context.hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_post(db: Session, post_id: int):
    return db.exec(select(Item).where(Item.id == post_id)).one()
    
def get_allposts(db: Session):
    return db.exec(select(Item)).all()

def create_post(db: Session, post: Item):
    post = Item(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post 

def remove_post(db: Session, post_id: int):
    post = db.exec(select(Item).where(Item.id == post_id)).one()
    db.delete(post)
    db.commit()
    return 