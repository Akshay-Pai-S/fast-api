from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
# from random import randrange
import psycopg
from psycopg.rows import dict_row, namedtuple_row
import time

class Post(BaseModel):
    id : int
    title : str
    content : str
    published : bool = False
    rating : int | None = None

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
    for i in my_posts:
        if i["id"]==id:
            return i

@app.get('/')
def root():
    return {'message':'Hello welcome hi sap'}

@app.get('/posts')
def get_posts():
    cur.execute("""select * from posts""")
    posts=cur.fetchall()
    return {'Posts' : posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(payload : Post):
    # post['id']=randrange(1,100000)
    post=payload.model_dump()
    my_posts.append(post)
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
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"Error" : f"The post with id : {id} not found"}
    return {"post" : post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post=find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    my_posts.remove(post)


@app.put('/posts/{id}')
def update_post(id : int, post : Post):
    p=find_post(id)
    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    ind=my_posts.index(p)
    post_dict=post.model_dump()
    my_posts[ind]=post_dict
    return {'updated' : post_dict}