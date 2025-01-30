from sqlalchemy import false, true
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


URL_DATABASE = 'postgresql+psycopg2://postgres:892255@localhost:5432/project'

engine = create_engine(
    URL_DATABASE
    )

SessionLocal = sessionmaker(autoflush=false, bind=engine)

Base = declarative_base()
