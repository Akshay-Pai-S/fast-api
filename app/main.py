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
my_posts : list=[{"tiltle":"dummy line", "content":"Dummy","id" : 0},{"title" : "First post", "content":"hi", "id":1}]

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
    cur.execute("""select * from posts where id = %s""", (id,))
    return cur.fetchone()

@app.get('/')
def root():
    return {'message':'Hello welcome hi sap'}

@app.get('/posts')
def get_posts():
    posts=cur.execute("""select * from posts""").fetchall()
    return {'Posts' : posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(payload : Post):
    cur.execute("""insert into posts (title, content, published) values (%s, %s, %s) returning * """, (payload.title, payload.content, payload.published))
    post=cur.fetchone()
    con.commit()
    return { 'post' : post}

@app.get('/posts/latest')
def get_latest():
    post=my_posts[-1]
    return {"last post" : post}

@app.get('/posts/{id}')
def get_post(id : int):
    post=find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    return {"post" : post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post=cur.execute("""delete from posts where id= %s returning *""",(id,)).fetchone()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    con.commit()

@app.put('/posts/{id}')
def update_post(id : int, payload : Post):
    post=cur.execute("""update posts set title=%s , content= %s , published=%s where id=%s returning * """, (payload.title, payload.content, payload.published, id)).fetchall()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    con.commit()
    return {'updated' : post}