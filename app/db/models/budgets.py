from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict

class Budget(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, 
        json_encoders={bytes: lambda v: v.hex()},  
        from_attributes=True 
    )

    id: str = Field(default=None, alias="_id")
    user_id: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=100)
    limit: float = Field(default=0.0)
    status: int = Field(default=0)
    currency: str = Field(default="VND")
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(default_factory=datetime.utcnow)
    description: str = Field(default="")
    tags: List[str] = Field(default_factory=list)   
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


  






