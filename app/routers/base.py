from fastapi import APIRouter
from app.routers.user import router as user


api_router = APIRouter()

api_router.include_router(user, prefix="/user", tags=["user"])


