"""
Game session routes for the mnist application.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
from ...models import GameSession, GameSessionResponse, GameRoomStatus, TokenRequest
from ..session import game_rooms, active_sessions, create_token, validate_token, get_room_status

router = APIRouter()


@router.post("/api/token", response_model=GameSessionResponse)
async def create_game_session() -> Dict:
    """
    Create a new game session.
    If there's a room waiting for a player, join that room.
    Otherwise, create a new room and wait for another player.
    
    Returns:
        A dictionary with the session token and room information
    """
    # Find a room with only one player
    waiting_room_id = None
    for room_id, sessions in game_rooms.items():
        if len(sessions) == 1:
            waiting_room_id = room_id
            break
    
    # If no waiting room, create a new one
    if waiting_room_id is None:
        room_id = str(uuid.uuid4())
        game_rooms[room_id] = []
        player_number = 1
        status = GameRoomStatus.WAITING
    else:
        room_id = waiting_room_id
        player_number = 2
        status = GameRoomStatus.FULL
    
    # Create a new session
    session = GameSession(
        room_id=room_id,
        player_number=player_number
    )
    
    # Store the session
    if room_id not in game_rooms:
        game_rooms[room_id] = []
    game_rooms[room_id].append(session)
    active_sessions[session.session_id] = session
    
    # Create a token
    token = create_token(session)
    
    return {
        "token": token,
        "room_id": room_id,
        "player_number": player_number,
        "status": status
    }


@router.post("/api/validate-token")
async def validate_session_token(request: TokenRequest) -> Dict:
    """
    Validate a session token.
    
    Args:
        request: The token validation request
        
    Returns:
        A dictionary with the validation result and session information
        
    Raises:
        HTTPException: If the token is invalid
    """
    session = validate_token(request.token)
    if session is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Check the room status
    status = get_room_status(session.room_id)
    
    return {
        "valid": True,
        "room_id": session.room_id,
        "player_number": session.player_number,
        "status": status
    }
