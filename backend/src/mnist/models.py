"""
Data models for the mnist application.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from enum import Enum
import uuid


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


class FortyTwoResponse(BaseModel):
    """Response model for the forty-two endpoint."""
    
    value: int = Field(
        description="The answer to the ultimate question of life, the universe, and everything"
    )


class GameRoomStatus(str, Enum):
    """Status of a game room."""
    WAITING = "waiting"
    FULL = "full"


class GameSession(BaseModel):
    """Model for a game session."""
    
    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the session"
    )
    room_id: str = Field(
        description="Identifier for the game room"
    )
    player_number: int = Field(
        description="Player number in the room (1 or 2)"
    )


class GameSessionResponse(BaseModel):
    """Response model for the game session endpoint."""
    
    token: str = Field(
        description="Session token for the player"
    )
    room_id: str = Field(
        description="Identifier for the game room"
    )
    player_number: int = Field(
        description="Player number in the room (1 or 2)"
    )
    status: GameRoomStatus = Field(
        description="Status of the game room"
    )


class TokenRequest(BaseModel):
    """Request model for token validation."""
    
    token: str = Field(
        description="Session token to validate"
    )
