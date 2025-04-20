from pydantic import BaseModel,EmailStr
from typing import Optional

# --- Request Models ----

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class ResetPassword(BaseModel):
    email:str
    password:str


# ---- Response Models ----

class UserRead(BaseModel):
    id:int
    name:str
    email:EmailStr


    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token:str
    token_type:str = 'bearer'


class TokenData(BaseModel):
    user_id: Optional[str] = None
