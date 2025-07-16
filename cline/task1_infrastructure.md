# Task 1: Getting to know the infrastructure

## Prompt:
Specialize the API server with a new API request which returns 42 and make sure the front-end is receiving it.  Project readme should be able to help you. Expand this context doc with what you learn.  

## Project Structure
This is a modern web application with React frontend and Python FastAPI backend.

- Backend: Python FastAPI in `backend/src/mnist/app.py`
- Frontend: React in `frontend/src/App.tsx`
- API Client: TypeScript in `frontend/src/api/client.ts`
- Models: Pydantic models in `backend/src/mnist/models.py`
- Types: Generated TypeScript types in `frontend/src/types/apiTypes.ts`

## Implementation Plan

1. Add a new Pydantic model `FortyTwoResponse` in `models.py` with an integer field `value`
2. Add a new GET endpoint `/api/forty-two` in `app.py` that returns `{"value": 42}`
3. Add a new method `getFortyTwo()` in the API client
4. Update the frontend to display the value from the new endpoint
5. Generate TypeScript types from the updated Pydantic models

## Type Generation
The project uses automatic TypeScript type generation from Python Pydantic models.
This ensures type safety between frontend and backend. After updating models.py,
run `npm run generate-types` in the frontend directory to update the TypeScript types.
