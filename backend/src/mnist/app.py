from fastapi import FastAPI
from typing import Dict
from .models import HelloResponse, ExampleRequest, ExampleResponse

app = FastAPI(title="mnist API")


@app.get("/api/hello", response_model=HelloResponse)
async def hello() -> Dict[str, str]:
    return {"message": "Hello from mnist API!"}


@app.post("/api/example", response_model=ExampleResponse)
async def create_example(request: ExampleRequest) -> Dict[str, str]:
    """Example endpoint to demonstrate request and response models."""
    # This is just a mock implementation
    return {
        "id": "123",
        "name": request.name,
        "created_at": "2023-01-01T00:00:00Z",
        "items": []
    }
