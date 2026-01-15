from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
# from random import randrange
import psycopg
from psycopg.rows import dict_row, namedtuple_row
import time

class Post(BaseModel):
    title : str
    content : str
    published : bool = False
    #rating : int | None = None

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

@app.get('/posts')
def get_posts():
    posts=cur.execute(t'select * from posts').fetchall()
    return {'Posts' : posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(payload : Post):
    post=cur.execute(
        t'insert into posts (title, content, published) values ({payload.title}, {payload.content}, {payload.published}) returning *'
        ).fetchone()
    con.commit()
    return { 'post' : post}

@app.get('/posts/latest/{limit}')
def get_latest(limit:int):
    post=cur.execute(t'select * from posts order by creation_time desc limit {limit}').fetchall()
    return {"last post" : post}

@app.get('/posts/{id}')
def get_post(id : int):
    post=find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    return {"post" : post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post=cur.execute(t'delete from posts where id= {id} returning *').fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    con.commit()

@app.put('/posts/{id}')
def update_post(id : int, payload : Post):
    post=cur.execute(
        t'update posts set title={payload.title} , content= {payload.content} , published={payload.published} where id={id} returning * '
        ).fetchall()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    con.commit()
    return {'updated' : post}