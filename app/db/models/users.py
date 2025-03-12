from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={bytes: lambda v: v.hex()},  
        from_attributes=True 
    )

    id: str = Field(default=None, alias="_id")
    username: str = Field(..., min_length=1, max_length=100)  
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str = Field(..., min_length=8, max_length=100)

   
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
   

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

   
    

  






