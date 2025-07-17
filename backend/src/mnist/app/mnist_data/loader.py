"""
Functions for loading and accessing the MNIST dataset.
"""

import gzip
import numpy as np
import random
from pathlib import Path
from typing import Tuple, List, Optional

from .constants import MNIST_DATASET_DIR
from .download import download_mnist_dataset

# In-memory storage for MNIST dataset
mnist_train_images = None
mnist_train_labels = None
mnist_test_images = None
mnist_test_labels = None


def load_mnist_images(filepath: Path) -> np.ndarray:
    """
    Load MNIST images from a gzipped file.
    
    Args:
        filepath: Path to the gzipped MNIST images file
        
    Returns:
        A numpy array of shape (num_images, 28, 28) with pixel values normalized to [0, 1]
    """
    with gzip.open(filepath, 'rb') as f:
        # First 16 bytes are magic number, number of images, rows, columns
        magic = int.from_bytes(f.read(4), 'big')
        num_images = int.from_bytes(f.read(4), 'big')
        num_rows = int.from_bytes(f.read(4), 'big')
        num_cols = int.from_bytes(f.read(4), 'big')
        
        # Read image data
        buf = f.read(num_images * num_rows * num_cols)
        data = np.frombuffer(buf, dtype=np.uint8).reshape(num_images, num_rows, num_cols)
        
        # Normalize to [0, 1]
        return data / 255.0


def load_mnist_labels(filepath: Path) -> np.ndarray:
    """
    Load MNIST labels from a gzipped file.
    
    Args:
        filepath: Path to the gzipped MNIST labels file
        
    Returns:
        A numpy array of shape (num_labels,) with label values (0-9)
    """
    with gzip.open(filepath, 'rb') as f:
        # First 8 bytes are magic number and number of labels
        magic = int.from_bytes(f.read(4), 'big')
        num_labels = int.from_bytes(f.read(4), 'big')
        
        # Read label data
        buf = f.read(num_labels)
        return np.frombuffer(buf, dtype=np.uint8)


def load_mnist_dataset() -> None:
    """
    Load the MNIST dataset into memory.
    """
    global mnist_train_images, mnist_train_labels, mnist_test_images, mnist_test_labels
    
    # Download dataset if not present
    download_mnist_dataset()
    
    # Load dataset
    train_images_path = MNIST_DATASET_DIR / "train-images-idx3-ubyte.gz"
    train_labels_path = MNIST_DATASET_DIR / "train-labels-idx1-ubyte.gz"
    test_images_path = MNIST_DATASET_DIR / "t10k-images-idx3-ubyte.gz"
    test_labels_path = MNIST_DATASET_DIR / "t10k-labels-idx1-ubyte.gz"
    
    mnist_train_images = load_mnist_images(train_images_path)
    mnist_train_labels = load_mnist_labels(train_labels_path)
    mnist_test_images = load_mnist_images(test_images_path)
    mnist_test_labels = load_mnist_labels(test_labels_path)
    
    print(f"Loaded MNIST dataset:")
    print(f"  Train images: {mnist_train_images.shape}")
    print(f"  Train labels: {mnist_train_labels.shape}")
    print(f"  Test images: {mnist_test_images.shape}")
    print(f"  Test labels: {mnist_test_labels.shape}")


def get_random_mnist_image(include_label: bool = True) -> Tuple[List[List[float]], Optional[int]]:
    """
    Get a random MNIST image from the dataset.
    
    Args:
        include_label: Whether to include the label in the response
        
    Returns:
        A tuple of (image, label) where image is a 28x28 array of pixel values
        and label is the digit (0-9) or None if include_label is False
    """
    global mnist_train_images, mnist_train_labels
    
    # Load dataset if not already loaded
    if mnist_train_images is None:
        load_mnist_dataset()
    
    # Get a random index
    idx = random.randint(0, len(mnist_train_images) - 1)
    
    # Get the image and label
    image = mnist_train_images[idx].tolist()
    label = int(mnist_train_labels[idx]) if include_label else None
    
    return image, label


def init_dataset():
    """
    Initialize the MNIST dataset.
    """
    try:
        load_mnist_dataset()
    except Exception as e:
        print(f"Error loading MNIST dataset: {e}")
        print("The dataset will be loaded on the first request.")
