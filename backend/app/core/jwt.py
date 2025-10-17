"""Clerk JWT verification and JWKS management."""
import httpx
import time
from jose import jwt
from typing import Dict, Optional
from app.core.logging import get_logger

logger = get_logger(__name__)


class ClerkJWKS:
    """Manages Clerk JWKS fetching and caching."""
    
    def __init__(self, jwks_url: str):
        self.jwks_url = jwks_url
        self._jwks: Optional[Dict] = None
        self._fetched_at: float = 0
        self._cache_duration = 12 * 3600  # 12 hours
    
    async def get(self) -> Dict:
        """
        Get JWKS, fetching from Clerk if cache is stale.
        
        Returns:
            JWKS dictionary
        """
        current_time = time.time()
        
        if not self._jwks or (current_time - self._fetched_at) > self._cache_duration:
            logger.info(f"Fetching JWKS from {self.jwks_url}")
            async with httpx.AsyncClient() as client:
                response = await client.get(self.jwks_url, timeout=10.0)
                response.raise_for_status()
                self._jwks = response.json()
                self._fetched_at = current_time
                logger.info("JWKS fetched and cached successfully")
        
        return self._jwks


# Global JWKS client instance
_jwks_client: Optional[ClerkJWKS] = None


def init_jwks_client(jwks_url: str) -> None:
    """Initialize the global JWKS client."""
    global _jwks_client
    _jwks_client = ClerkJWKS(jwks_url)
    logger.info(f"JWKS client initialized with URL: {jwks_url}")


async def verify_clerk_jwt(token: str) -> Dict:
    """
    Verify a Clerk JWT token.
    
    Args:
        token: The JWT token to verify
        
    Returns:
        Decoded JWT payload containing user information
        
    Raises:
        ValueError: If token is invalid or verification fails
    """
    if _jwks_client is None:
        raise ValueError("JWKS client not initialized. Call init_jwks_client first.")
    
    try:
        # Get JWKS
        jwks = await _jwks_client.get()
        
        # Get the key ID from token header
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        
        if not kid:
            raise ValueError("Token missing 'kid' in header")
        
        # Find the matching key in JWKS
        key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
        
        if key is None:
            raise ValueError(f"No matching JWK found for kid: {kid}")
        
        # Decode and verify the token
        payload = jwt.decode(
            token,
            key,
            algorithms=[key.get("alg", "RS256")],
            options={
                "verify_aud": False,  # Clerk uses multiple audiences
                "verify_iss": True,
            }
        )
        
        logger.debug(f"Successfully verified JWT for user: {payload.get('sub')}")
        return payload
        
    except jwt.JWTError as e:
        logger.warning(f"JWT verification failed: {str(e)}")
        raise ValueError(f"Invalid JWT: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {str(e)}")
        raise ValueError(f"JWT verification error: {str(e)}")
