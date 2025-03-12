from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict

class Investment(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={bytes: lambda v: v.hex()},  
        from_attributes=True 
    )

    id: str = Field(default=None, alias="_id")
    user_id: str = Field(..., min_length=1, max_length=100)
    investment_type: str = Field(..., min_length=1, max_length=100)
    asset_name: str = Field(..., min_length=1, max_length=100)
    symbol: str = Field(..., min_length=1, max_length=100)
    buy_price: float = Field(default=0.0)
    current_price: float = Field(default=0.0)
    quantity: float = Field(default=0.0)
    total_invested: float = Field(default=0.0)
    current_value: float = Field(default=0.0)
    roi: float = Field(default=0.0)
    buy_date: datetime = Field(default_factory=datetime.utcnow)
    status: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
   

   
   
    

  






