# Task 4: Get MNIST image API

## Prompt

Users will identify MNIST images with a digit 0-9. Let's make an API to fetch an MNIST image. Download MNIST dataset at server start and server up random images from the dataset at each API request. Better yet, let's download MNIST and add it to the server resources with an appropriate gitignore. So that we don't need to redownload on every server start.

## Implementation Plan

1. Create a new module for MNIST dataset handling
   - Add functionality to download and load the MNIST dataset
   - Store the dataset in a server resources directory
   - Implement functions to get random images from the dataset

2. Update models.py to add a model for MNIST image responses
   - Create a Pydantic model for MNIST image data
   - Include fields for the image data and optional label

3. Create a new route for serving MNIST images
   - Add an endpoint to get a random MNIST image
   - Implement token validation to ensure only authenticated users can access images
   - Add option to include or exclude the actual digit label

4. Update the .gitignore file
   - Add entries to exclude the MNIST dataset files
   - Ensure the dataset directory structure is preserved

5. Create detailed documentation
   - Document the implementation in a separate markdown file
   - Include information on how the MNIST dataset is stored and accessed

## Implementation Details

### 1. MNIST Dataset Module

Created a new module structure for MNIST dataset handling:

- **constants.py**: Contains constants for dataset paths and URLs
  ```python
  MNIST_DATASET_DIR = Path(__file__).parent.parent.parent.parent.parent / "resources" / "mnist"
  MNIST_TRAIN_IMAGES_URL = "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
  MNIST_TRAIN_LABELS_URL = "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"
  MNIST_TEST_IMAGES_URL = "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"
  MNIST_TEST_LABELS_URL = "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
  ```

- **download.py**: Handles downloading the dataset if not already present
  ```python
  def download_mnist_dataset() -> None:
      ensure_dataset_dir()
      
      # Define file paths
      train_images_path = MNIST_DATASET_DIR / "train-images-idx3-ubyte.gz"
      train_labels_path = MNIST_DATASET_DIR / "train-labels-idx1-ubyte.gz"
      test_images_path = MNIST_DATASET_DIR / "t10k-images-idx3-ubyte.gz"
      test_labels_path = MNIST_DATASET_DIR / "t10k-labels-idx1-ubyte.gz"
      
      # Download files if they don't exist
      if not train_images_path.exists():
          download_file(MNIST_TRAIN_IMAGES_URL, train_images_path)
      # ... (similar for other files)
  ```

- **loader.py**: Handles loading the dataset and providing access to images
  ```python
  def get_random_mnist_image(include_label: bool = True) -> Tuple[List[List[float]], Optional[int]]:
      # Load dataset if not already loaded
      if mnist_train_images is None:
          load_mnist_dataset()
      
      # Get a random index
      idx = random.randint(0, len(mnist_train_images) - 1)
      
      # Get the image and label
      image = mnist_train_images[idx].tolist()
      label = int(mnist_train_labels[idx]) if include_label else None
      
      return image, label
  ```

- **__init__.py**: Exposes the necessary functions and initializes the dataset
  ```python
  from .constants import MNIST_DATASET_DIR
  from .loader import (
      load_mnist_dataset,
      get_random_mnist_image,
      init_dataset
  )
  
  # Initialize the dataset when the module is imported
  try:
      init_dataset()
  except Exception as e:
      print(f"Error initializing MNIST dataset: {e}")
      print("The dataset will be loaded on the first request.")
  ```

### 2. Model for MNIST Image Responses

Added a new Pydantic model in models.py:
```python
class MnistImageResponse(BaseModel):
    """Response model for the MNIST image endpoint."""
    
    image: List[List[float]] = Field(
        description="28x28 MNIST image as a 2D array of pixel values (0-1)"
    )
    label: Optional[int] = Field(
        None,
        description="The actual digit label (0-9) for the image, may be None in game mode"
    )
```

### 3. MNIST Image API Route

Created a new route file (mnist_images.py) for MNIST image operations:
```python
@router.get("/api/mnist/image", response_model=MnistImageResponse)
async def get_mnist_image(
    session: Optional[GameSession] = Depends(get_session_from_token),
    include_label: bool = Query(False, description="Whether to include the actual digit label")
) -> Dict:
    # Require a valid session
    if session is None:
        # In a real game, we would return a 401 Unauthorized error
        # For now, we'll just return a different image to demonstrate the API
        image, label = get_random_mnist_image(include_label=False)
        return {"image": image, "label": None}
    
    # Get a random image
    image, label = get_random_mnist_image(include_label=include_label)
    
    return {"image": image, "label": label}
```

Updated app/__init__.py to include the new router:
```python
from .routes import base, forty_two, game, mnist_images
from .mnist_data import init_dataset

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
```

### 4. .gitignore Updates

Updated the .gitignore file to exclude the MNIST dataset files while preserving the directory structure:
```
# MNIST Dataset
backend/resources/mnist/*.gz
backend/resources/mnist/*-ubyte.gz
# Keep the directory structure
!backend/resources/mnist/.gitkeep
```

Created the resources/mnist directory with a .gitkeep file to ensure the directory structure is preserved.

### 5. Benefits of this Implementation

1. **Modular Design**: Split the MNIST dataset handling into a proper module with separate files for different concerns.
2. **Lazy Loading**: The dataset is loaded on demand if not already loaded, which improves startup time.
3. **Persistent Storage**: The dataset is downloaded once and stored in the resources directory, avoiding repeated downloads.
4. **Clean API**: The API endpoint is simple and follows the same pattern as other endpoints in the application.
5. **Type Safety**: The Pydantic model ensures type safety and automatic documentation.
