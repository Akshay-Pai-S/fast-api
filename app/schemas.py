from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

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
    
    model_config= ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponce(BaseModel):
    id: int
    email : EmailStr
    created_at: datetime

    model_config= ConfigDict(from_attributes=True)