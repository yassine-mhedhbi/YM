import os 
from dotenv import load_dotenv 
from pathlib import Path 
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

load_dotenv(dotenv_path=Path('.') / '.env')

engine = create_engine(os.getenv('DATABASE_URI'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
