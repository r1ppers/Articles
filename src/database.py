from typing import Annotated
from sqlalchemy import false
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Depends


URL_DATABASE = 'postgresql://postgres:892255@db:5432/project'

engine = create_engine(
    URL_DATABASE
    )

SessionLocal = sessionmaker(autoflush=false, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependence = Annotated[Session, Depends(get_db)]