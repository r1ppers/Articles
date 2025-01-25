from sqlalchemy import false, true
from config import host, user, password, db_name
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


URL_DATABASE = 'postgresql://postgres:892255@localhost:5432/project'

engine = create_engine(
    URL_DATABASE
    )

SessionLocal = sessionmaker(autoflush=false, bind=engine)

Base = declarative_base()
