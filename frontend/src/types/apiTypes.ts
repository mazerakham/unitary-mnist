/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

/**
 * Status of the game room
 */
export type GameRoomStatus = "waiting" | "full";

/**
 * Example request model to demonstrate type generation.
 */
export interface ExampleRequest {
  /**
   * Name of the user
   */
  name: string;
  /**
   * Email address of the user
   */
  email?: string | null;
  /**
   * User preferences as key-value pairs
   */
  preferences?: {
    [k: string]: string;
  } | null;
}
/**
 * Example response model to demonstrate type generation.
 */
export interface ExampleResponse {
  /**
   * Unique identifier for the created resource
   */
  id: string;
  /**
   * Name of the user
   */
  name: string;
  /**
   * Timestamp when the resource was created
   */
  created_at: string;
  /**
   * List of associated items
   */
  items?: string[] | null;
}
/**
 * Response model for the forty-two endpoint.
 */
export interface FortyTwoResponse {
  /**
   * The answer to the ultimate question of life, the universe, and everything
   */
  value: number;
}
/**
 * Model for a game session.
 */
export interface GameSession {
  /**
   * Unique identifier for the session
   */
  session_id?: string;
  /**
   * Identifier for the game room
   */
  room_id: string;
  /**
   * Player number in the room (1 or 2)
   */
  player_number: number;
}
/**
 * Response model for the game session endpoint.
 */
export interface GameSessionResponse {
  /**
   * Session token for the player
   */
  token: string;
  /**
   * Identifier for the game room
   */
  room_id: string;
  /**
   * Player number in the room (1 or 2)
   */
  player_number: number;
  status: GameRoomStatus;
}
/**
 * Response model for the hello endpoint.
 */
export interface HelloResponse {
  /**
   * Greeting message from the API
   */
  message: string;
}
/**
 * Request model for token validation.
 */
export interface TokenRequest {
  /**
   * Session token to validate
   */
  token: string;
}
