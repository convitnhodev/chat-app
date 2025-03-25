from fastapi import WebSocket
from typing import Optional, Tuple
from app.core.config import settings
from jose import JWTError, jwt

async def get_token_from_socket(websocket: WebSocket) -> Optional[str]:
    """Extract token from query parameters or Authorization header"""
    try:
        # Try to get token from query parameter
        token = websocket.query_params.get('token')

        # If no token in query params, try Authorization header
        if not token: 
            auth_header = websocket.headers.get('authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        return token
    except Exception:
        return None

async def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        
        if not payload.get('sub'): 
            return None
            
        user_data = {
            'username': payload.get('sub'),  
            'role': payload.get('role', 'user'), 
            'sub': payload.get('sub')  
        }
            
        return user_data
    except JWTError as e:
        print(f"JWT decode error: {str(e)}")
        return None
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None

async def authenticate_websocket(websocket: WebSocket) -> Tuple[bool, Optional[dict]]:
    """Authenticate WebSocket connection using token"""
    try:
        # Get token from either source
        token = await get_token_from_socket(websocket)
        if not token:
            print("No token found")
            return False, None

        # Verify token and get payload
        user_data = await verify_token(token)
        if not user_data:
            print("Invalid token or payload")
            return False, None

        print(f"Authentication successful for user: {user_data['username']}")
        return True, user_data

    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return False, None
        