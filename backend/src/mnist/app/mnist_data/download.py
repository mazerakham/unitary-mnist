"""
Functions for downloading the MNIST dataset.
"""

import os
import urllib.request
from pathlib import Path
from .constants import (
    MNIST_DATASET_DIR,
    MNIST_TRAIN_IMAGES_URL,
    MNIST_TRAIN_LABELS_URL,
    MNIST_TEST_IMAGES_URL,
    MNIST_TEST_LABELS_URL
)


def ensure_dataset_dir() -> None:
    """
    Ensure the MNIST dataset directory exists.
    """
    os.makedirs(MNIST_DATASET_DIR, exist_ok=True)


def download_file(url: str, filepath: Path) -> None:
    """
    Download a file from a URL to a local filepath.
    
    Args:
        url: The URL to download from
        filepath: The local filepath to save to
    """
    print(f"Downloading {url} to {filepath}")
    urllib.request.urlretrieve(url, filepath)


def download_mnist_dataset() -> None:
    """
    Download the MNIST dataset if not already present.
    """
    ensure_dataset_dir()
    
    # Define file paths
    train_images_path = MNIST_DATASET_DIR / "train-images-idx3-ubyte.gz"
    train_labels_path = MNIST_DATASET_DIR / "train-labels-idx1-ubyte.gz"
    test_images_path = MNIST_DATASET_DIR / "t10k-images-idx3-ubyte.gz"
    test_labels_path = MNIST_DATASET_DIR / "t10k-labels-idx1-ubyte.gz"
    
    # Download files if they don't exist
    if not train_images_path.exists():
        download_file(MNIST_TRAIN_IMAGES_URL, train_images_path)
    
    if not train_labels_path.exists():
        download_file(MNIST_TRAIN_LABELS_URL, train_labels_path)
    
    if not test_images_path.exists():
        download_file(MNIST_TEST_IMAGES_URL, test_images_path)
    
    if not test_labels_path.exists():
        download_file(MNIST_TEST_LABELS_URL, test_labels_path)
