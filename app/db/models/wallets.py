from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict

class Wallet(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={bytes: lambda v: v.hex()},  
        from_attributes=True 
    )

    id: str = Field(default=None, alias="_id")
    user_id: str = Field(..., min_length=1, max_length=100)
    balance: float = Field(default=0.0)
    currency: str = Field(default="VND")
    status: int = Field(default=0)
    name: str = Field(default="")
   
   
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
   

   
   
    

  






