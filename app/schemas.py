from datetime import datetime
from pydantic import BaseModel

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
    
    class Config:
        from_attributes = True