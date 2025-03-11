from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import EmailStr, Field, BaseModel, ConfigDict


class UserAccess(BaseModel): 
    anon: int = 0 
    auth: int = 47 


class UserPhoto(BaseModel):
    data: bytes
    type: str = Field(..., pattern="^(jpg|jpeg|png|gif)$")  # Validate image types


class UserPublic(BaseModel):
    fn: str = Field(..., min_length=1, max_length=100)  # Add length validation
    photo: Optional[UserPhoto] = None


class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,  # Allow population by alias
        json_encoders={bytes: lambda v: v.hex()},  # Convert bytes to hex string
        from_attributes=True  # Allow ORM mode
    )

    id: str = Field(default=None, alias="_id")
    access: UserAccess = Field(default_factory=UserAccess)
    createdat: datetime = Field(default_factory=datetime.utcnow)
    updatedat: datetime = Field(default_factory=datetime.utcnow)
    lastseen: datetime = Field(default_factory=datetime.utcnow)
    stateat: Optional[datetime] = None

    state: int = Field(default=0, ge=0, le=2)  # Add value validation

    devices: Optional[Dict[str, Any]] = None
    useragent: Optional[str] = None

    public: UserPublic

    tags: List[str] = Field(default_factory=list)

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

    def update_lastseen(self):
        """Update last seen timestamp"""
        self.lastseen = datetime.utcnow()
        self.updatedat = self.lastseen

    @classmethod
    def create_new(cls, email: str, full_name: str) -> "User":
        """Factory method to create a new user"""
        now = datetime.utcnow()
        return cls(
            createdat=now,
            updatedat=now,
            lastseen=now,
            public=UserPublic(fn=full_name),
            tags=[f"email:{email}"]
        )






