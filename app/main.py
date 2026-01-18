from typing import List
from fastapi import Depends, FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
# from random import randrange
import psycopg
from psycopg.rows import dict_row, namedtuple_row
import time

from sqlalchemy import desc

from app import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas

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
    #posts=cur.execute(t'select * from posts').fetchall()
    posts=db.query(models.Post).all()
    return posts

@app.post('/posts',status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_posts(payload : schemas.PostCreate, db: Session = Depends(get_db)):
    # post=cur.execute(
    #     t'insert into posts (title, content, published) values ({payload.title}, {payload.content}, {payload.published}) returning *'
    #     ).fetchone()
    # con.commit()
    post=models.Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get('/posts/latest/{limit}', response_model=List[schemas.PostResponce])
def get_latest(limit:int, db: Session = Depends(get_db)):
    # post=cur.execute(t'select * from posts order by creation_time desc limit {limit}').fetchall()
    post=db.query(models.Post).order_by(desc(models.Post.created_at)).limit(limit).all()
    return post

@app.get('/posts/{id}', response_model=schemas.PostResponce)
def get_post(id : int, db: Session = Depends(get_db)):
    # post=find_post(id)
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    return post

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    # post=cur.execute(t'delete from posts where id= {id} returning *').fetchone()
    # con.commit()
    post=db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    post.delete(synchronize_session=False)
    db.commit()

@app.put('/posts/{id}', response_model=schemas.PostResponce)
def update_post(id : int, payload : schemas.PostCreate, db: Session = Depends(get_db)):
    # post=cur.execute(
    #     t'update posts set title={payload.title} , content= {payload.content} , published={payload.published} where id={id} returning * '
    #     ).fetchall()
    # con.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    post=post_query.first()
    return post