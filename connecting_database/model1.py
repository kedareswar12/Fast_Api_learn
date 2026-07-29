from sqlalchemy import Integer , String, Column , Table , Boolean
from database import Base 


class TodoModel(Base):
  __tablename__ = "todos"
  id = Column(Integer, primary_key=True , index = True)
  title = Column(String(100), index = True)
  descripition  = Column(String(500) , nullable= True , index  =True)
  completed = Column(Boolean, index=True , default=bool)