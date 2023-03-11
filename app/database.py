from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# A URL that we use to connect to database. this command says where our database located in our system
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port} /{settings.database_name}"

# this engine is responsible to connect to postgres database/ establishing a connection to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#when we talk to a database we usually use a session to do that
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all of our models(tables) that we are going to define later are going to inherit from this base mopdel below/ 
# our models actually are going to be an extended version of below base class
Base = declarative_base()

# Dependency # get a session to talk to our database. everytime we get a request to our API endpoints, we're gonna get a session.
#and once we're done, we close it.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password=940202, cursor_factory=RealDictCursor)
#         c = conn.cursor()
#         print('Connection to database Succesfull!!!')
#         break

#     except Exception as Error:
#         print('Connection to database Unsuccesfull!!!')
#         time.sleep(3)
