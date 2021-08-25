from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

Base = declarative_base()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise NotImplementedError

engine = create_engine(DATABASE_URL)

Session = scoped_session(sessionmaker(bind=engine, autocommit=True, autoflush=True))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
