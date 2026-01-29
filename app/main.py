from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
# from random import randrange
import psycopg
from psycopg.rows import dict_row, namedtuple_row
import time

from sqlalchemy import select, desc

from app import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

while True:
    try:
        con=psycopg.connect(host='localhost', dbname='fastapi', user='postgres' ,password='postgres', row_factory=dict_row)
        cur=con.cursor()
        print('DB connection success')
        break
    except Exception as error:
        print(f'DB connection failed\nERROR : {error}')
        time.sleep(3)

def find_post(id:int):
    cur.execute(t'select * from posts where id = {id}')
    return cur.fetchone()

@app.get('/')
def root():
    return {'message':'Hello welcome hi sap'}

@app.get('/posts', response_model=List[schemas.PostResponce])
def get_posts(db: Session = Depends(get_db)):
    stmt=select(models.Post)
    posts=db.execute(stmt).scalars().all()
    return posts

@app.post('/posts',status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_posts(payload : schemas.PostCreate, db: Session = Depends(get_db)):
    post=models.Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get('/posts/latest/{limit}', response_model=List[schemas.PostResponce])
def get_latest(limit:int, db: Session = Depends(get_db)):
    stmt=select(models.Post).order_by(models.Post.created_at.desc()).limit(limit)
    posts=db.execute(stmt).scalars().all()
    return posts

@app.get('/posts/{id}', response_model=schemas.PostResponce)
def get_post(id : int, db: Session = Depends(get_db)):
    stmt=select(models.Post).where(models.Post.id==id)
    post=db.execute(stmt).scalar_one_or_none()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    return post

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    post=db.get(models.Post, id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    db.delete(post)
    db.commit()

@app.put('/posts/{id}', response_model=schemas.PostResponce)
def update_post(id : int, payload : schemas.PostCreate, db: Session = Depends(get_db)):
    post=db.get(models.Post,id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    for k,v in payload.model_dump().items():
        setattr(post,k,v)
    db.commit()
    db.refresh(post)
    return post

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponce)
def create_user(payload : schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pswd=utils.hash(payload.password)
    payload.password=hashed_pswd
    user=models.User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/users', response_model=List[schemas.UserResponce])
def get_users(db: Session = Depends(get_db)):
    stmt=select(models.User)
    result=db.execute(stmt)
    users=result.scalars().all()
    return users