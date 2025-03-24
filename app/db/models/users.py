from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict, field_validator
from datetime import date

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str = Field(default="user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    dob: Optional[str] = None

    @field_validator('dob')
    def validate_dob(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, "%d/%m/%Y")
            return v
        except ValueError:
            raise ValueError("Date must be in format DD/MM/YYYY")

class User(UserBase):
    id: str = Field(default=None, alias="_id")
    hashed_password: str
    dob: Optional[str] = None
    disabled: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('dob')
    def validate_dob(cls, v):
        if v is None:
            return None
        if isinstance(v, datetime):
            return v.strftime("%d/%m/%Y")
        return v

    class Config:
        populate_by_name = True
        json_encoders = {
            date: lambda v: v.strftime("%d/%m/%Y") if v else None
        }

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[str] = None
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            date: lambda v: v.strftime("%d/%m/%Y") if v else None
        }

    @property
    def email(self) -> Optional[str]:
        """Extract email from tags"""
        for tag in self.tags:
            if tag.startswith('email:'):
                return tag[6:]
        return None
    
    @property
    def phone(self) -> Optional[str]:
        """Extract phone from tags"""
        for tag in self.tags:
            if tag.startswith('tel:'):
                return tag[4:]
        return None

  






