import axios from 'axios';
import { 
  ExampleRequest, 
  ExampleResponse, 
  HelloResponse, 
  FortyTwoResponse,
  GameSessionResponse,
  TokenRequest
} from '../types/apiTypes';

// Create an axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Store the session token
let sessionToken: string | null = null;

// Add token to requests if available
api.interceptors.request.use(config => {
  if (sessionToken) {
    config.headers['token'] = sessionToken;
  }
  return config;
});

/**
 * API client for interacting with the backend
 */
export const apiClient = {
  /**
   * Get a hello message from the API
   */
  getHello: async (): Promise<HelloResponse> => {
    const response = await api.get<HelloResponse>('/hello');
    return response.data;
  },

  /**
   * Create an example resource
   * @param data The request data
   */
  createExample: async (data: ExampleRequest): Promise<ExampleResponse> => {
    const response = await api.post<ExampleResponse>('/example', data);
    return response.data;
  },

  /**
   * Get the answer to the ultimate question
   * Returns 42 if a valid session token is available, otherwise 43
   */
  getFortyTwo: async (): Promise<FortyTwoResponse> => {
    const response = await api.get<FortyTwoResponse>('/forty-two');
    return response.data;
  },

  /**
   * Create a new game session
   * If there's a room waiting for a player, join that room
   * Otherwise, create a new room and wait for another player
   */
  createGameSession: async (): Promise<GameSessionResponse> => {
    const response = await api.post<GameSessionResponse>('/token');
    // Store the token for future requests
    sessionToken = response.data.token;
    return response.data;
  },

  /**
   * Validate a session token
   * @param token The token to validate
   */
  validateToken: async (token: string): Promise<any> => {
    const response = await api.post('/validate-token', { token } as TokenRequest);
    return response.data;
  },

  /**
   * Set the session token manually
   * @param token The token to set
   */
  setSessionToken: (token: string | null): void => {
    sessionToken = token;
  },

  /**
   * Get the current session token
   */
  getSessionToken: (): string | null => {
    return sessionToken;
  },
};
