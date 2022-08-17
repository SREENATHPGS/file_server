print("Initilializing models.")
import os, secrets, string, json
from .custom_exceptions import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER=os.environ.get('POSTGRES_USER', 'file_manager')
POSTGRES_PW=os.environ.get('POSTGRES_PW', 'dbpw')
POSTGRES_URL=os.environ.get('POSTGRES_URL', '0.0.0.0:5432')
POSTGRES_DB=os.environ.get('POSTGRES_DB', 'data_manager')
DB_URL = f'sqlite:///{POSTGRES_DB}.db' #'postgresql+psycopg2://{user}:{password}@{url}/{db}'.format(user=POSTGRES_USER, password=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

Base = declarative_base()
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()


def getApiKey(length = 6):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

def create_tables(tablename = '*'):
    print("Creating tables.")
    if tablename == '*':
        Base.metadata.create_all(engine)