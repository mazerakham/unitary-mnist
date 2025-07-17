"""
Constants for MNIST dataset handling.
"""

from pathlib import Path

# Constants for MNIST dataset
MNIST_DATASET_DIR = Path(__file__).parent.parent.parent.parent.parent / "resources" / "mnist"
MNIST_TRAIN_IMAGES_URL = "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
MNIST_TRAIN_LABELS_URL = "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"
MNIST_TEST_IMAGES_URL = "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"
MNIST_TEST_LABELS_URL = "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
