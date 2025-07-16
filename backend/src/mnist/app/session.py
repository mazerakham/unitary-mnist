"""
Session management for the mnist application.
"""

from typing import Dict, List, Optional
import base64
import json
from ..models import GameSession, GameRoomStatus

# In-memory storage for game rooms and sessions
# In a production environment, this would be a database
game_rooms: Dict[str, List[GameSession]] = {}
active_sessions: Dict[str, GameSession] = {}


def create_token(session: GameSession) -> str:
    """
    Create a token from a session object.
    
    Args:
        session: The game session to encode in the token
        
    Returns:
        A base64 encoded token containing the session data
    """
    session_data = {
        "session_id": session.session_id,
        "room_id": session.room_id,
        "player_number": session.player_number
    }
    # Encode the session data as a base64 string
    # In a production environment, this would be signed with a secret key
    token_bytes = json.dumps(session_data).encode('utf-8')
    return base64.b64encode(token_bytes).decode('utf-8')


def validate_token(token: str) -> Optional[GameSession]:
    """
    Validate a token and return the associated session.
    
    Args:
        token: The token to validate
        
    Returns:
        The associated game session if valid, None otherwise
    """
    try:
        # Decode the token
        token_bytes = base64.b64decode(token)
        session_data = json.loads(token_bytes.decode('utf-8'))
        
        # Check if the session exists
        session_id = session_data.get("session_id")
        if session_id in active_sessions:
            return active_sessions[session_id]
        return None
    except Exception:
        return None


def get_room_status(room_id: str) -> GameRoomStatus:
    """
    Get the status of a game room.
    
    Args:
        room_id: The ID of the room to check
        
    Returns:
        The status of the room (WAITING or FULL)
    """
    if room_id in game_rooms and len(game_rooms[room_id]) == 2:
        return GameRoomStatus.FULL
    return GameRoomStatus.WAITING
