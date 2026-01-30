from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas, utils

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponce)
def create_user(payload : schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pswd=utils.hash(payload.password)
    payload.password=hashed_pswd
    user=models.User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/', response_model=List[schemas.UserResponce])
def get_users(db: Session = Depends(get_db)):
    stmt=select(models.User)
    result=db.execute(stmt)
    users=result.scalars().all()
    return users

@router.get('/{id}', response_model=schemas.UserResponce)
def get_user(id: int, db: Session = Depends(get_db)):
    user=db.get(models.User, id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id: {id} is not found")
    return user