from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings
settings=Settings()
#Configuration with database (as the IP we can use image name since everything will bbe in docker container)
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.userdb}:{settings.password}@{settings.host}:{settings.port}/{settings.database}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()