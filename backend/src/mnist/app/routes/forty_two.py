"""
Forty-two route for the mnist application.
"""

from fastapi import APIRouter, Depends, Header
from typing import Dict, Optional
from ...models import FortyTwoResponse, GameSession
from ..session import validate_token

router = APIRouter()


async def get_session_from_token(token: Optional[str] = Header(None)) -> Optional[GameSession]:
    """
    Dependency to get the session from a token header.
    
    Args:
        token: The session token from the request header
        
    Returns:
        The associated game session if valid, None otherwise
    """
    if token is None:
        return None
    return validate_token(token)


@router.get("/api/forty-two", response_model=FortyTwoResponse)
async def forty_two(session: Optional[GameSession] = Depends(get_session_from_token)) -> Dict[str, int]:
    """
    Endpoint that returns the answer to the ultimate question.
    Returns 42 if a valid session token is provided, otherwise 43.
    
    Args:
        session: The game session from the token header
        
    Returns:
        A dictionary with the answer value
    """
    if session is None:
        return {"value": 43}
    return {"value": 42}
