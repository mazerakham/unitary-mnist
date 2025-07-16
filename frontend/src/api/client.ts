import axios from 'axios';
import { ExampleRequest, ExampleResponse, HelloResponse } from '../types/apiTypes';

// Create an axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
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
};
