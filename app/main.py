from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

@app.get('/')
def root():
    return {'message':'Hello welcome hi sap'}

app.include_router(post.router)
app.include_router(user.router)