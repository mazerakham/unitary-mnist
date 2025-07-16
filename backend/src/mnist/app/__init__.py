"""
Application module for the mnist application.
"""

from fastapi import FastAPI
from .routes import base, forty_two, game

# Create the FastAPI application
app = FastAPI(title="mnist API")

# Include the routers
app.include_router(base.router)
app.include_router(forty_two.router)
app.include_router(game.router)
