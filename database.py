from sqlalchemy import create_engine as _create_engine
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHAMY_DATABASE_URL ='sqlite:///./mydatabase.db'

engine=_create_engine(SQLALCHAMY_DATABASE_URL,connect_args={
   "check_same_thread":False 
})

SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)


Base=_declarative_base()


