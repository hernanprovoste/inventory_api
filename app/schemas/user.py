from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User Email", min_length=3, max_length=50)
    password: str = Field(..., description="User Password", min_length=6, max_length=64)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        model_config = ConfigDict(from_attributes = True) # Change because it will deprecated in Pydantic V3