"""
MNIST image routes for the mnist application.
"""

from fastapi import APIRouter, Depends, Header, Query
from typing import Dict, Optional
from ...models import MnistImageResponse, GameSession
from ..session import validate_token
from ..mnist_data import get_random_mnist_image

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


@router.get("/api/mnist/image", response_model=MnistImageResponse)
async def get_mnist_image(
    session: Optional[GameSession] = Depends(get_session_from_token),
    include_label: bool = Query(False, description="Whether to include the actual digit label")
) -> Dict:
    """
    Get a random MNIST image.
    
    Args:
        session: The game session from the token header
        include_label: Whether to include the actual digit label
        
    Returns:
        A dictionary with the image data and optional label
    """
    # Require a valid session
    if session is None:
        # In a real game, we would return a 401 Unauthorized error
        # For now, we'll just return a different image to demonstrate the API
        image, label = get_random_mnist_image(include_label=False)
        return {"image": image, "label": None}
    
    # Get a random image
    image, label = get_random_mnist_image(include_label=include_label)
    
    return {"image": image, "label": label}
