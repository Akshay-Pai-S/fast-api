from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router=APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(payload: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    stmt=select(models.User).where(models.User.email==payload.username)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Invalid User E-Mail')

    if not utils.verify(payload.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Incorrect Password')
    
    access_token=oauth2.create_access_token(
        data={"user_id": user.id}
    )
    
    return {"token" : access_token, "token_type": "Bearer"}