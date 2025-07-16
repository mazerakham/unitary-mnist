import React, { useState, useEffect } from 'react';
import { apiClient } from './api/client';

function App() {
  const [message, setMessage] = useState<string>('Loading...');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHello = async () => {
      try {
        const response = await apiClient.getHello();
        setMessage(response.message);
      } catch (err) {
        console.error('Error fetching hello message:', err);
        setError('Failed to fetch message from API');
      }
    };

    fetchHello();
  }, []);

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
          <p>
            <strong>Message from API:</strong> {message}
          </p>
        )}
      </div>

      <div className="card">
        <h2>Getting Started</h2>
        <p>
          Edit <code>frontend/src/App.tsx</code> and save to reload the frontend.
        </p>
        <p>
          Edit <code>backend/src/mnist/app.py</code> to modify the API.
        </p>
        <p>
          Run <code>npm run generate-types</code> to update TypeScript types from Pydantic models.
        </p>
      </div>
    </div>
  );
}

export default App;
