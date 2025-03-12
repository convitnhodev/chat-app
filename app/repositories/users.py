from datetime import datetime
from typing import Optional
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models.users import User, UserCreate

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users

    async def create_user(self, user_data: UserCreate) -> User:
    
        now = datetime.utcnow()
        user_dict = {
            "user_id": str(ObjectId()),  # Generate new ObjectId
            "balance": 0.0,
            "currency": "VND",
            "status": 0,
            "name": user_data.name,
            "created_at": now,
            "updated_at": now
        }

        # Insert into database
        result = await self.collection.insert_one(user_dict)
        
        # Fetch and return the created user
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return User(**created_user)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        """
        user = await self.collection.find_one({"_id": user_id})
        return User(**user) if user else None

    async def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Get user by name
        """
        user = await self.collection.find_one({"name": name})
        return User(**user) if user else None

    async def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """
        Update user information
        """
        update_data["updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
        
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete user
        """
        result = await self.collection.delete_one({"_id": user_id})
        return result.deleted_count > 0 