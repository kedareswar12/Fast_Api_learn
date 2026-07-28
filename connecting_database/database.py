import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
load_dotenv()
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus


DB_PASSWORD = os.getenv("DB_PASSWORD")
# print(os.getenv("FOO"))
# DATABASE_URL = os.getenv("DATABASE_URL")
print(DB_PASSWORD)

engine = create_engine(
    "mysql+mysqlconnector://root:%s@localhost:3306/mydatabase" % quote_plus(DB_PASSWORD)
)
metadat = MetaData()

Sessionlocal = sessionmaker(autocommit = False , autoflush = False , bind = engine)
# this is the session maker object 
with engine.connect() as conn:
    print("Connected successfully")


Base = declarative_base()

