import datetime
from typing import List, Optional

from pydantic import BaseModel
from fastapi import Body


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    body: str


class PostCreate(PostBase):
    user_id: int


class PostList(PostBase):
    created_date: Optional[datetime.datetime]
    owner_id: int
    owner: UserBase

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    name: str
    body: str
    email: str


class CommentList(CommentBase):
    id: int
    post_id: int
    created_date: Optional[datetime.datetime] = Body(None)

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
