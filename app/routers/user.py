from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.core.security import create_access_token
from app.core.config import settings
from datetime import timedelta
from jose import JWTError, jwt
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import UserService
from app.core.hashing import Hasher
from app.const.error_detail import ErrorDetail
from app.core.schemas import StandardResponse
from app.db.models.users import UserCreate, UserResponse


router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(), user_service: UserService = Depends(UserService)):
   
    user = await user_service.get_user_by_username(form_data.username)
  
    if not user or not Hasher.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorDetail.INVALID_PASSWORD,
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
   
    return StandardResponse(
        success=True,
        message="Login successful",
        data={
            "access_token": access_token,
            "token_type": "Bearer",
            "expiresIn": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "username": user.username,
        }
    )
   
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


@router.post("/register", response_model=StandardResponse[UserResponse])
async def register_user(user: UserCreate, user_service: UserService = Depends(UserService)):
    try:
        # Add logging to debug the incoming request
        print(f"Received user data: {user.dict()}")
        
        new_user = await user_service.create_user(user)
        
        return StandardResponse(
            success=True,
            message="User registered successfully",
            data=UserResponse.from_orm(new_user)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log the actual error for debugging
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )
    

@router.get("/users/{user_id}")
async def get_user(user_id: str, user_service: UserService = Depends(UserService)) -> StandardResponse[UserResponse]:
    try:
        user = await user_service.get_user_by_id(user_id)
        if not user:
            return StandardResponse(
                success=False,
                message="User not found",
                error="User with specified ID does not exist"
            )
        return StandardResponse(
            success=True,
            message="User retrieved successfully",
            data=user
        )
    except Exception as e:
        return StandardResponse(
            success=False,
            message="Failed to retrieve user",
            error=str(e)
        )




