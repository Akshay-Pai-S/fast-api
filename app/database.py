from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from .config import settings

database_url=f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(database_url, echo=True)

SessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine, class_=Session)

class Base(DeclarativeBase):
    pass

#dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()