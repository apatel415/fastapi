from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    '''Respose model for user create output'''
    id: int 
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class PostBase(BaseModel):
    '''Standardizes what data a post should contain.
    It will automatically validate that the post contains proper data'''
    title: str
    content: str
    published: bool = True # default set to true
    # rating: Optional[int] = None # optional field that defaults to none
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    '''Class is used in the response mode; it determines what fields of the data is returned'''
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    # converts the sql alchemy model into a pydantic model
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    
    # less than or equal to 1; could not figure out how to restrict to just 0 and 1
    dir: conint(le=1)