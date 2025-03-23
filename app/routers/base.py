from fastapi import APIRouter
from app.routers.router_login import router as login_router


api_router = APIRouter()

api_router.include_router(login_router, prefix="/login", tags=["login"])


