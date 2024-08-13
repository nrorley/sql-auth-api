from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    id: str

class UserCreate(UserBase):
    key : str
    session: str
    mint : str
    auth_token : str

class User(UserBase):
    id: str
    key : str
    session: str
    mint : str

    class Config:
        orm_mode = True

class updateUser(BaseModel):
    key : Optional[str] 
    session: Optional[str]
    mint : Optional[str]
    auth_token : str

    class Config:
        orm_mode = True

class authToken(BaseModel):
    auth_token: str