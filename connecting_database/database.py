import os
from dotenv import load_dotenv # to create the environment variables 
from sqlalchemy import create_engine, MetaData
# create engine helps us to connect the python language to the database and then the metadata is the additional data describing about the actual data 
'''
| Roll No | Name  | Age |
| ------- | ----- | --- |
| 1       | Kedar | 21  |
| 2       | Rahul | 20  |


Table Name : Students

Columns:
Roll No  → Integer
Name     → String
Age      → Integer

# the above mentioned data is the meta data from table name 
'''
load_dotenv()
from sqlalchemy.orm import sessionmaker , session
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

DB_USER = "kedar"
DB_NAME = "mydatabase"
DB_PASSWORD = os.getenv("DB_PASSWORD")
# print(os.getenv("FOO"))
DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@localhost:3306/{DB_NAME}"
)
print(DB_PASSWORD)

# engine = create_engine(
#     "mysql+mysqlconnector://root:%s@localhost:3306/mydatabase" % quote_plus(DB_PASSWORD)
# )

engine = create_engine(DATABASE_URL)
metadata = MetaData()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# this is the session maker object 
with engine.connect() as conn:
    print("Connected successfully")


Base = declarative_base()

