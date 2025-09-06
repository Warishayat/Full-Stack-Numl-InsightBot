from fastapi import FastAPI
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


Database_url = os.getenv("POSTGRES_SQL_DATABASE_URL")


engine = create_engine(Database_url)
Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


# to get the session of database
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
