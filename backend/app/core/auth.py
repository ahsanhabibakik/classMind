"""FastAPI authentication dependencies."""
from typing import Dict, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt import verify_clerk_jwt
from app.core.logging import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    FastAPI dependency to get the current authenticated user.
    
    Extracts and verifies the JWT token from the Authorization header.
    
    Args:
        credentials: HTTP Bearer credentials containing the JWT token
        
    Returns:
        Dictionary containing user_id and email
        
    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    token = credentials.credentials
    
    try:
        payload = await verify_clerk_jwt(token)
        
        # Extract user information
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing 'sub' claim")
        
        email = payload.get("email")
        
        user_info = {
            "user_id": user_id,
            "email": email or "",
        }
        
        logger.info(f"User authenticated: {user_id}")
        return user_info
        
    except ValueError as e:
        logger.warning(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, str]]:
    """
    Optional authentication dependency.
    
    Returns user info if token is present and valid, None otherwise.
    Useful for endpoints that can work with or without authentication.
    
    Args:
        credentials: Optional HTTP Bearer credentials
        
    Returns:
        User dictionary if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
