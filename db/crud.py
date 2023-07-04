from sqlmodel import Session, select
from passlib.context import CryptContext
from db.models import Project, SuperUserCreate, SuperUser, Create_Project
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


def get_project(db: Session, id: int):
    item = db.exec(select(Project).where(Project.id == id)).one()
    if not item:
        raise HTTPException(status_code=404, detail="not found")
    return item


def get_allprojects(db: Session):
    return db.exec(select(Project)).all()


def remove_project(db: Session, id: int):
    db_project = get_project(db, id)
    db.delete(db_project)
    db.commit()
    return db_project


def update_project(db: Session, id: int, item: Project):
    db_project = get_project(db, id)
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def create_project(db: Session, project: Create_Project):
    project = Project(**project.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
