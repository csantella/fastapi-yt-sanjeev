from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field 
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase): 
    published: bool


class PostResponse(BaseModel):
    post: Post = Field(alias="Post", serialization_alias='post') # make sure lowercase 'post' maps to 'Post'
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class Vote(BaseModel):
    post_id: int
    direction: Annotated[int, Field(strict=True, ge=0, le=1)]

