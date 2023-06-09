from urllib import parse
from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine=create_engine(SQLALCHEMY_DATABASE_URL)


 


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()


# while True:
#     try:
#         conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Pa@121001', cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database Connection was succesfull")
#         break
#     except Exception as error:
#         print("connecting to database failed") 
#         print("Error: ",error)
#         time.sleep(2)

