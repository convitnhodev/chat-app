
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    phone: str
    address: str
    dob: str
    role: str = Field(default="user")

    @validator('dob')
    def validate_dob(cls, v):
        try:
            # Convert string to date object
            return datetime.strptime(v, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Date must be in format DD/MM/YYYY")

class User(BaseModel):
    id: str = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[str] = None
    role: str = Field(default="user")
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: str
    address: str
    dob: datetime
    role: str
    created_at: datetime

    class Config:
        populate_by_name = True



