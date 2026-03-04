from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False
    #rating : int | None = None

class PostCreate(PostBase):
    pass

class PostResponce(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponce
    
    model_config= ConfigDict(from_attributes=True)

class PostWithVotes(BaseModel):
    Post: PostResponce
    votes: int
    
    model_config= ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponce(BaseModel):
    id: int
    email : EmailStr
    created_at: datetime

    model_config= ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]