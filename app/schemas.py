from datetime import datetime
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: Annotated[str, StringConstraints(pattern=r'^\+?[0-9]{10,15}$')]

class UserResponce(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone_number: str
    created_at: datetime

    model_config= ConfigDict(from_attributes=True)

class UserResponceAll(BaseModel):
    name: str
    email: EmailStr

    model_config= ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title : Annotated[str, StringConstraints(min_length=1, max_length=200)]
    content : Annotated[str, StringConstraints(min_length=1, max_length=5000)]
    published : bool = True
    #rating : int | None = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponce
    
    model_config= ConfigDict(from_attributes=True)

class PostWithVotes(BaseModel):
    Post: PostResponse
    votes: int
    
    model_config= ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
