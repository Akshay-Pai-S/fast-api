from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostResponce])
def get_posts(db: Session = Depends(get_db)):
    stmt=select(models.Post)
    posts=db.execute(stmt).scalars().all()
    return posts

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_posts(payload : schemas.PostCreate, db: Session = Depends(get_db)):
    post=models.Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get('/latest/{limit}', response_model=List[schemas.PostResponce])
def get_latest(limit:int, db: Session = Depends(get_db)):
    stmt=select(models.Post).order_by(models.Post.created_at.desc()).limit(limit)
    posts=db.execute(stmt).scalars().all()
    return posts

@router.get('/{id}', response_model=schemas.PostResponce)
def get_post(id : int, db: Session = Depends(get_db)):
    stmt=select(models.Post).where(models.Post.id==id)
    post=db.execute(stmt).scalar_one_or_none()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    return post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    post=db.get(models.Post, id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    db.delete(post)
    db.commit()

@router.put('/{id}', response_model=schemas.PostResponce)
def update_post(id : int, payload : schemas.PostCreate, db: Session = Depends(get_db)):
    post=db.get(models.Post,id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    for k,v in payload.model_dump().items():
        setattr(post,k,v)
    db.commit()
    db.refresh(post)
    return post
