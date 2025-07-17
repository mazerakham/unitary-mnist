"""
Application module for the mnist application.
"""

from fastapi import FastAPI
from .routes import base, forty_two, game, mnist_images
from .mnist_data import init_dataset

# Create the FastAPI application
app = FastAPI(title="mnist API")

# Include the routers
app.include_router(base.router)
app.include_router(forty_two.router)
app.include_router(game.router)
app.include_router(mnist_images.router)

# Initialize the MNIST dataset
try:
    init_dataset()
except Exception as e:
    print(f"Error initializing MNIST dataset: {e}")
    print("The dataset will be loaded on the first request.")
