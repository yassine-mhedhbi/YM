import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path('.') / '.env')
engine = create_engine(os.getenv('DATABASE_URI'))


def get_session():
    with Session(engine) as session:
        yield session
