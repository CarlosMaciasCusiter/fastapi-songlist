from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class SongBase(BaseModel):
    title: str
    artist: str
    single: bool = False


class SongCreate(SongBase):
    pass


class Song(SongBase):
    id: int
    uploaded_AT: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class Vote(BaseModel):
    song_id: int
    dir: conint(le=1)


class SongOut(BaseModel):
    Songs: Song
    votes: int

    class Config:
        orm_mode = True
