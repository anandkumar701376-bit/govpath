from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRegister(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    mobile_number: Optional[str] = Field(None, max_length=15)


class TokenPayload(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    mobile_number: Optional[str] = None
    created_at: datetime


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    mobile_number: Optional[str] = Field(None, max_length=15)
    profile_image: Optional[str] = None
