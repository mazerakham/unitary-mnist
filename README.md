# mnist

A modern web application with React frontend and Python FastAPI backend.

## Project Structure

```
mnist/
├── backend/         # Python FastAPI backend
├── frontend/        # React frontend
├── scripts/         # Utility scripts
└── cline/           # Cline context for AI assistance
```

## Getting Started

### Prerequisites

- Node.js (v16+)
- npm or yarn
- Python (v3.8+)
- pip

### Setup

1. **Backend Setup**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
pip install -r requirements.txt
```

2. **Frontend Setup**

```bash
cd frontend
npm install
```

### Running the Application

You can run both the frontend and backend with a single command:

```bash
./scripts/run_project.sh
```

This will start:
- Backend server at http://localhost:8000
- Frontend development server at http://localhost:3000

### Manual Startup

If you prefer to run the servers manually:

**Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn mnist.app:app --reload
```

**Frontend:**
```bash
cd frontend
npm start
```

## Development

- Backend API documentation is available at http://localhost:8000/docs
- Edit `frontend/src/App.tsx` to modify the React frontend
- Edit `backend/src/mnist/app.py` to modify the FastAPI backend

### TypeScript Type Generation

This project supports automatic TypeScript type generation from Python Pydantic models. This ensures type safety and consistency between your frontend and backend.

To generate TypeScript types from your Pydantic models:

```bash
cd frontend
npm run generate-types
```

This will create TypeScript interfaces in `frontend/src/types/apiTypes.ts` based on the Pydantic models defined in `backend/src/mnist/models.py`.

An example of the generated TypeScript interfaces is provided in `frontend/src/types/apiTypes.ts.example`.

Usage example:

```typescript
import { ExampleRequest, ExampleResponse } from './types/apiTypes';

// Now you have type-safe API interactions
const submitForm = async (data: ExampleRequest): Promise<ExampleResponse> => {
  const response = await axios.post<ExampleResponse>('/api/example', data);
  return response.data;
};
```

## Testing

**Backend Tests:**
```bash
cd backend
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## License

This project is open source and available under the [MIT License](LICENSE).
