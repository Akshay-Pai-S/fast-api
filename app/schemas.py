from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
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
    phone_number : Annotated[str, StringConstraints(pattern=r'^\+?[0-9]{10,15}$')]

class UserResponce(BaseModel):
    id: int
    email : EmailStr
    phone_number: str
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