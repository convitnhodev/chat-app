from datetime import datetime
from typing import Optional, Union
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from app.schemas.user import User, UserCreate
from app.core.hashing import Hasher
from app.db.session import get_db

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db)) -> None:
        self.db = db
        self.collection = db.users

    def _format_dob(self, dob: Union[str, datetime, None]) -> Optional[str]:
        """Format DOB to string consistently"""
        if dob is None:
            return None
        if isinstance(dob, datetime):
            return dob.strftime("%d/%m/%Y")
        return dob
    
   
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        if user_doc := await self.collection.find_one({"username": username}):
            return User(**user_doc)
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        if user_doc := await self.collection.find_one({"email": email}):
            return User(**user_doc)
        return None
    
    async def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        try:
            # Check if email exists
            if await self.get_user_by_email(user.email):
                raise ValueError("Email already registered")

            # Check if username exists
            if await self.get_user_by_username(user.username):
                raise ValueError("Username already taken")

            # Create user document
            now = datetime.utcnow()
           
            user_dict = {
                "_id": str(ObjectId()),
                "username": user.username,
                "email": user.email,
                "hashed_password": user.password,
                "name": user.name,
                "phone": user.phone,
                "address": user.address,
                "dob": user.dob,
                "role": user.role,
                "disabled": False,
                "created_at": now,
                "updated_at": now
            }

            # Insert into database
            await self.collection.insert_one(user_dict)
            
            # Return user object
            return User(**user_dict)
            
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")
    
       

 