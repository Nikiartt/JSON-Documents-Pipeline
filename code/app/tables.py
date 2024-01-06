from sqlalchemy import Column ,Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
    
class User_table(Base):#By declarative_base class we create a new table.
    __tablename__='users'
    id = Column(Integer, primary_key=True, nullable=False,unique=True,autoincrement=True)#Create unique values column of ID.
    username = Column(String, nullable=False,unique=True)
    password= Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))