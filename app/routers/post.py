from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, oauth2

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostResponce])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    stmt=select(models.Post)
    posts=db.execute(stmt).scalars().all()
    return posts

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_posts(payload : schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post=models.Post(owner_id = current_user.id, **payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.get('/myposts/', response_model=List[schemas.PostResponce])
def get_my_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    stmt=select(models.Post).where(models.Post.owner_id==current_user.id)
    posts=db.execute(stmt).scalars().all()
    return posts

@router.get('/myposts/{id}', response_model=schemas.PostResponce)
def get_post(id : int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    stmt=select(models.Post).where(models.Post.id==id)
    post=db.execute(stmt).scalar_one_or_none()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Not Authorised to perform requested action in {id}')
    return post

@router.get('/latest', response_model=List[schemas.PostResponce])
def get_latest(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str =''):
    stmt=select(models.Post).order_by(models.Post.created_at.desc()).limit(limit).offset(skip).filter(models.Post.title.ilike(f"%{search}%"))
    posts=db.execute(stmt).scalars().all()
    return posts

@router.get('/{id}', response_model=schemas.PostResponce)
def get_post(id : int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    stmt=select(models.Post).where(models.Post.id==id)
    post=db.execute(stmt).scalar_one_or_none()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'id {id} not found')
    return post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post=db.get(models.Post, id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Not Authorised to perform requested action in {id}')
    db.delete(post)
    db.commit()

@router.put('/{id}', response_model=schemas.PostResponce)
def update_post(id : int, payload : schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post=db.get(models.Post,id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {id} not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Not Authorised to perform requested action in {id}')
    
    for k,v in payload.model_dump().items():
        setattr(post,k,v)
    db.commit()
    db.refresh(post)
    return post
