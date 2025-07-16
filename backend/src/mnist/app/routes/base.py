"""
Base routes for the mnist application.
"""

from fastapi import APIRouter
from typing import Dict
from ...models import HelloResponse, ExampleRequest, ExampleResponse

router = APIRouter()


@router.get("/api/hello", response_model=HelloResponse)
async def hello() -> Dict[str, str]:
    """
    Hello endpoint that returns a greeting message.
    
    Returns:
        A dictionary with a greeting message
    """
    return {"message": "Hello from mnist API!"}


@router.post("/api/example", response_model=ExampleResponse)
async def create_example(request: ExampleRequest) -> Dict[str, str]:
    """
    Example endpoint to demonstrate request and response models.
    
    Args:
        request: The example request data
        
    Returns:
        A mock example response
    """
    # This is just a mock implementation
    return {
        "id": "123",
        "name": request.name,
        "created_at": "2023-01-01T00:00:00Z",
        "items": []
    }
