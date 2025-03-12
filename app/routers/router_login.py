from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from core.security import create_access_token
from core.config import settings
from datetime import timedelta


router = APIRouter()
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    # get user from db 
    user = None 
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    
    access_token_expire = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRATION_EXPIRE)
    access_token = create_access_token(data={"sub" : user.username, "owner" : user.owner}, expires_delta=access_token_expire)
     
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expiresIn": settings.ACCESS_TOKEN_EXPIRATION_EXPIRE,
        "username": user.username,
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")




