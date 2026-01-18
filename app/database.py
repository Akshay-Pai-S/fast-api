from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url='postgresql+psycopg://postgres:postgres@localhost/fastapi'

engine = create_engine(database_url, echo=True)

SessioLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base=declarative_base()

#dependency
def get_db():
    db=SessioLocal()
    try:
        yield db
    finally:
        db.close