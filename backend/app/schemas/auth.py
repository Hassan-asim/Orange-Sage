"""
Authentication schemas
"""

from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    username: str
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    expires_in: int
