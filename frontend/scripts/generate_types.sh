#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Set explicit Poetry bin path and Python path
export POETRY_BIN="$HOME/.local/bin/poetry"
export PYTHONPATH="$PROJECT_ROOT/backend/src:$PYTHONPATH"

# Function to display colored output
echo_colored() {
  local color=$1
  local message=$2
  case $color in
    "green") echo -e "\033[0;32m$message\033[0m" ;;
    "blue") echo -e "\033[0;34m$message\033[0m" ;;
    "yellow") echo -e "\033[0;33m$message\033[0m" ;;
    "red") echo -e "\033[0;31m$message\033[0m" ;;
    *) echo "$message" ;;
  esac
}

# Ensure Poetry is installed
if ! command -v poetry &> /dev/null; then
  # Run the poetry installation script
  source "$PROJECT_ROOT/scripts/install_poetry.sh"
  
  # Add Poetry to PATH for this session
  export PATH="$HOME/.local/bin:$PATH"
fi

# Install json-schema-to-typescript if needed
if ! npm list -g json-schema-to-typescript &> /dev/null; then
  echo_colored "yellow" "Installing json-schema-to-typescript globally (required for pydantic2-to-typescript)..."
  npm install -g json-schema-to-typescript
fi

# Ensure pydantic2-to-typescript is installed
cd "$PROJECT_ROOT/backend"

# Check if the package is already installed
if ! poetry run pip list | grep -q "pydantic2-to-typescript"; then
  echo_colored "yellow" "Installing pydantic2-to-typescript package..."
  
  # Try to install the package in the tools group
  poetry add --group tools pydantic2-to-typescript || {
    echo_colored "red" "Failed to install pydantic2-to-typescript using Poetry."
    echo_colored "yellow" "Trying alternative installation method..."
    
    # Activate the Poetry environment and install directly with pip
    poetry run pip install pydantic2-to-typescript
  }
fi

# Verify the package is installed
if ! poetry run pip list | grep -q "pydantic2-to-typescript"; then
  echo_colored "red" "Failed to install pydantic2-to-typescript."
  echo_colored "yellow" "Please install it manually with:"
  echo_colored "blue" "cd $PROJECT_ROOT/backend && poetry run pip install pydantic2-to-typescript"
  exit 1
fi

echo_colored "yellow" "Generating TypeScript types from Pydantic models..."
cd "$PROJECT_ROOT/backend" && $POETRY_BIN run python -c "from pydantic2ts import generate_typescript_defs; generate_typescript_defs('mnist.models', '../frontend/src/types/apiTypes.ts')"

if [ $? -eq 0 ]; then
  echo_colored "green" "TypeScript types generated successfully!"
else
  echo_colored "red" "Failed to generate TypeScript types."
  echo_colored "yellow" "This could be due to missing dependencies or configuration issues."
  echo_colored "yellow" "Please check that json-schema-to-typescript is installed globally:"
  echo_colored "blue" "npm install -g json-schema-to-typescript"
  
  # Debug information
  echo_colored "yellow" "Debugging information:"
  echo_colored "blue" "Python path:"
  $POETRY_BIN run python -c "import sys; print(sys.path)"
  echo_colored "blue" "Installed packages:"
  $POETRY_BIN run pip list | grep pydantic
  exit 1
fi
