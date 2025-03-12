from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict

class Subscription(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={bytes: lambda v: v.hex()},  
        from_attributes=True 
    )

    id: str = Field(default=None, alias="_id")
    user_id: str = Field(..., min_length=1, max_length=100)
    service_name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(default=0.0)
    currency: str = Field(default="VND")
    payment_method: str = Field(..., min_length=1, max_length=100)
    billing_cycle: str = Field(..., min_length=1, max_length=100)
    next_billing_date: datetime = Field(default_factory=datetime.utcnow)
    status: int = Field(default=0)
    category: str = Field(..., min_length=1, max_length=100)
    note: str = Field(default="")
   
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
   

   
   
    

  






