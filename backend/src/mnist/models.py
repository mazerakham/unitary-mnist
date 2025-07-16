"""
Data models for the mnist application.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class HelloResponse(BaseModel):
    """Response model for the hello endpoint."""
    
    message: str = Field(
        description="Greeting message from the API"
    )


class ExampleRequest(BaseModel):
    """Example request model to demonstrate type generation."""
    
    name: str = Field(
        description="Name of the user"
    )
    email: Optional[str] = Field(
        None,
        description="Email address of the user"
    )
    preferences: Optional[Dict[str, str]] = Field(
        None,
        description="User preferences as key-value pairs"
    )


class ExampleResponse(BaseModel):
    """Example response model to demonstrate type generation."""
    
    id: str = Field(
        description="Unique identifier for the created resource"
    )
    name: str = Field(
        description="Name of the user"
    )
    created_at: str = Field(
        description="Timestamp when the resource was created"
    )
    items: Optional[List[str]] = Field(
        default_factory=list,
        description="List of associated items"
    )
