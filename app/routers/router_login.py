from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.core.security import create_access_token
from app.core.config import settings
from datetime import timedelta
from app.db.session import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from jose import JWTError, jwt
from app.repositories.users import UserRepository
from app.schemas.user import UserResponse, UserCreate


router = APIRouter()
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(), db: AsyncIOMotorDatabase = Depends(get_db)):
    user_repo = UserRepository(db)
   
    user = await user_repo.get_user_by_username(form_data.username)
    if not user or not user_repo.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
   
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expiresIn": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "username": user.username,
    }
   
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None: 
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_username(username)
    if user is None: 
        raise credentials_exception
    
    return user


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    user_repo = UserRepository(db)

    if await user_repo.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    try: 
        user = await user_repo.create_user(user_data)
        return user 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )
    


        




