import React, { useState, useEffect } from 'react';
import { apiClient } from './api/client';
import { GameSessionResponse } from './types/apiTypes';

function App() {
  const [message, setMessage] = useState<string>('Loading...');
  const [fortyTwoValue, setFortyTwoValue] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [gameSession, setGameSession] = useState<GameSessionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch hello message
        const helloResponse = await apiClient.getHello();
        setMessage(helloResponse.message);
        
        // Fetch forty-two value
        const fortyTwoResponse = await apiClient.getFortyTwo();
        setFortyTwoValue(fortyTwoResponse.value);
      } catch (err) {
        console.error('Error fetching data from API:', err);
        setError('Failed to fetch data from API');
      }
    };

    fetchData();
  }, []);

  const handleCreateSession = async () => {
    setLoading(true);
    try {
      const session = await apiClient.createGameSession();
      setGameSession(session);
      // Refresh the forty-two value to demonstrate token validation
      const fortyTwoResponse = await apiClient.getFortyTwo();
      setFortyTwoValue(fortyTwoResponse.value);
    } catch (err) {
      console.error('Error creating game session:', err);
      setError('Failed to create game session');
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshFortyTwo = async () => {
    setLoading(true);
    try {
      const fortyTwoResponse = await apiClient.getFortyTwo();
      setFortyTwoValue(fortyTwoResponse.value);
    } catch (err) {
      console.error('Error fetching forty-two value:', err);
      setError('Failed to fetch forty-two value');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Welcome to mnist</h1>
        <p>A React + FastAPI application</p>
      </div>

      <div className="card">
        <h2>Backend Connection Test</h2>
        {error ? (
          <div style={{ color: 'red' }}>
            {error}
            <p>
              Make sure your backend server is running at http://localhost:8000
            </p>
          </div>
        ) : (
          <>
            <p>
              <strong>Message from API:</strong> {message}
            </p>
            <p>
              <strong>The answer to the ultimate question:</strong> {fortyTwoValue}
              {' '}
              <button 
                onClick={handleRefreshFortyTwo} 
                disabled={loading}
              >
                Refresh
              </button>
              {' '}
              {fortyTwoValue === 42 ? (
                <span style={{ color: 'green' }}>✓ Valid token</span>
              ) : (
                <span style={{ color: 'orange' }}>⚠ No valid token</span>
              )}
            </p>
          </>
        )}
      </div>

      <div className="card">
        <h2>Game Session</h2>
        {gameSession ? (
          <div>
            <p><strong>Room ID:</strong> {gameSession.room_id}</p>
            <p><strong>Player Number:</strong> {gameSession.player_number}</p>
            <p><strong>Status:</strong> {gameSession.status}</p>
            <p><strong>Token:</strong> <code>{gameSession.token.substring(0, 20)}...</code></p>
          </div>
        ) : (
          <p>No active game session. Create one to get a token.</p>
        )}
        <button 
          onClick={handleCreateSession} 
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Create Game Session'}
        </button>
      </div>

      <div className="card">
        <h2>Getting Started</h2>
        <p>
          Edit <code>frontend/src/App.tsx</code> and save to reload the frontend.
        </p>
        <p>
          Edit <code>backend/src/mnist/app/</code> to modify the API.
        </p>
        <p>
          Run <code>npm run generate-types</code> to update TypeScript types from Pydantic models.
        </p>
      </div>
    </div>
  );
}

export default App;
