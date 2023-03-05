from sqlmodel import Session, select
from passlib.context import CryptContext
from db.models import Item, SuperUserCreate, SuperUser, Post, Project
from fastapi import HTTPException


def get_user(db: Session, username: str):
    return db.exec(select(SuperUser).where(SuperUser.username == username)).one()


def get_allusers(db: Session):
    return db.exec(select(SuperUser)).all()


def create_user(db: Session, user: SuperUserCreate, pwd_context: CryptContext):
    user.password = pwd_context.hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_item(db: Session, id: int):
    item = db.exec(select(Item).where(Item.id == id)).one()
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item


def remove_item(db: Session, id: int):
    post = get_item(db, id)
    db.delete(post)
    db.commit()
    return post


def update_item(db: Session, id: int, item: Item):
    db_post = get_item(db, id)
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_post, key, value)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_allposts(db: Session):
    return db.exec(select(Item).where(Item.isProject == False)).all()


def get_allprojects(db: Session):
    return db.exec(select(Item).where(Item.isProject == True)).all()


def create_post(db: Session, post: Item):
    post = Item(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def create_project(db: Session, project: Project):
    project = Item(**project.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
