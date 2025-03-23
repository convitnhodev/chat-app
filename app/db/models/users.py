from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[str] = None  # Optional date of birth
    role: str = Field(default="user")

    @validator('dob')
    def validate_dob(cls, v):
        if v is None:
            return None
        try:
            datetime.strptime(v, "%d/%m/%Y")
            return v
        except ValueError:
            raise ValueError("Date must be in format DD/MM/YYYY")

class User(BaseModel):
    id: str = Field(default=None, alias="_id")
    username: str
    email: EmailStr
    hashed_password: str
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[str] = None
    role: str = Field(default="user")
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

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
    dob: Optional[date] = None
    role: str
    created_at: datetime

    class Config:
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

  






