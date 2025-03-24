from app.repositories.users import UserRepository
from app.schemas.user import User, UserCreate
from fastapi import Depends
from app.core.hashing import Hasher

class UserService:
    user_repo: UserRepository
    def __init__(self, user_repo: UserRepository = Depends(UserRepository)) -> None:
        self.user_repo = user_repo

    async def create_user(self, user: UserCreate) -> User:
        user.password = Hasher.get_password_hash(user.password)
        return await self.user_repo.create_user(user)
    
    async def get_user_by_username(self, username: str) -> User:
        return await self.user_repo.get_user_by_username(username)
    
    async def get_user_by_email(self, email: str) -> User:
        return await self.user_repo.get_user_by_email(email)
    
   
        
    
    
