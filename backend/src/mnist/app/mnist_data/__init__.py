"""
MNIST dataset handling module for the mnist application.
"""

from .constants import MNIST_DATASET_DIR
from .loader import (
    load_mnist_dataset,
    get_random_mnist_image,
    init_dataset
)

__all__ = [
    'MNIST_DATASET_DIR',
    'load_mnist_dataset',
    'get_random_mnist_image',
    'init_dataset'
]

# Initialize the dataset when the module is imported
try:
    init_dataset()
except Exception as e:
    print(f"Error initializing MNIST dataset: {e}")
    print("The dataset will be loaded on the first request.")
