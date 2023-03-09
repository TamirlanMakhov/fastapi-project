from datetime import datetime

from pydantic import BaseModel, EmailStr, validator


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True



class PostVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class Vote(BaseModel):
    post_id: int
    dir: int

    @validator('dir')
    def must_be_one_or_zero(cls, value):
        if value not in (0, 1):
            raise ValueError("Must be either 1 or 0")
        return value
