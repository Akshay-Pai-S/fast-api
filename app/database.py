from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

database_url='postgresql+psycopg://postgres:postgres@localhost/fastapi'

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