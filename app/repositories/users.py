from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.user import User, UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
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
                "hashed_password": self.get_password_hash(user.password),
                "full_name": user.full_name,
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
    
       

 