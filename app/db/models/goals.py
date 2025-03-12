from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict


class Transaction(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(default=0.0)
    currency: str = Field(default="VND")
    note: str = Field(default="")
    tags: List[str] = Field(default_factory=list)
    date: datetime = Field(default_factory=datetime.utcnow)

class Goal(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={bytes: lambda v: v.hex()},  
        from_attributes=True 
    )

    id: str = Field(default=None, alias="_id")
    user_id: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)
    target_amount: float = Field(default=0.0)
    current_amount: float = Field(default=0.0)
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(default_factory=datetime.utcnow)
    status: int = Field(default=0)
    category: str = Field(..., min_length=1, max_length=100)
    transactions: List[Transaction] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
   

   
   
    

  






