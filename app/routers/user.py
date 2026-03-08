from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from .. import models, schemas, utils, oauth2

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
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    db.refresh(user)
    return user

#Future plan: To improve based on the roles
@router.get('/', response_model=List[schemas.UserResponceAll])
def get_users(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    stmt=select(models.User)
    result=db.execute(stmt)
    users=result.scalars().all()
    return users

@router.get('/{id}', response_model=schemas.UserResponce)
def get_user(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    if id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Not Authorised to perform requested action')
    user=db.get(models.User, id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id: {id} is not found")
    return user