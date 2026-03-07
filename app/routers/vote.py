from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, oauth2

router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post=db.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f'id {vote.post_id} not found')

    stmt=select(models.Vote).where(models.Vote.post_id==vote.post_id , models.Vote.user_id==current_user.id)
    found_vote=db.execute(stmt).scalar_one_or_none()
    if vote.dir == 1 :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} has already liked the post {vote.post_id}.')
        db.add(models.Vote(post_id=vote.post_id, user_id=current_user.id))
        db.commit()
        return {'message' : 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Vote for post {vote.post_id} does not exists for user {current_user.id}')
        db.delete(found_vote)
        db.commit()
        return {'message' : 'successfully deleted vote'}