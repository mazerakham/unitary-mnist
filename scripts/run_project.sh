#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

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

# Setup Python environment with Poetry
if [ ! -d "$PROJECT_ROOT/backend/.venv" ]; then
  echo_colored "yellow" "Setting up Python virtual environment with Poetry..."
  cd "$PROJECT_ROOT/backend"
  
  # Configure Poetry to create virtual environment in project directory
  poetry config virtualenvs.in-project true --local
  
  # Install dependencies
  poetry install
  cd "$PROJECT_ROOT"
fi

# Install frontend dependencies
echo_colored "yellow" "Installing frontend dependencies..."
cd "$PROJECT_ROOT/frontend"
npm install --legacy-peer-deps
cd "$PROJECT_ROOT"

# Ensure types directory exists
mkdir -p "$PROJECT_ROOT/frontend/src/types"

# Generate TypeScript types if they don't exist
if [ ! -f "$PROJECT_ROOT/frontend/src/types/apiTypes.ts" ]; then
  echo_colored "yellow" "Generating TypeScript types from Pydantic models..."
  cd "$PROJECT_ROOT/frontend"
  npm run generate-types || echo_colored "yellow" "Type generation skipped. Run manually with 'npm run generate-types' after setup."
  cd "$PROJECT_ROOT"
fi

# Check if TypeScript types exist
if [ ! -f "$PROJECT_ROOT/frontend/src/types/apiTypes.ts" ]; then
  echo_colored "red" "ERROR: TypeScript type definitions file not found!"
  echo_colored "yellow" "You need to generate TypeScript types before running the application."
  echo_colored "yellow" "Run the following command to generate types:"
  echo_colored "blue" "cd $PROJECT_ROOT/frontend && npm run generate-types"
  echo_colored "yellow" "Remember to run this command whenever you make changes to the API models."
  exit 1
fi

echo_colored "green" "Starting mnist application..."

# Check if concurrently is available
if [ ! -f "$PROJECT_ROOT/frontend/node_modules/.bin/concurrently" ]; then
  echo_colored "red" "ERROR: concurrently not found in node_modules."
  echo_colored "yellow" "Make sure frontend dependencies are installed correctly."
  echo_colored "blue" "Try running: cd $PROJECT_ROOT/frontend && npm install"
  exit 1
fi

# Check if port 8000 is already in use
BACKEND_PORT=8000
if command -v lsof &> /dev/null; then
  if lsof -i :$BACKEND_PORT -t &> /dev/null; then
    echo_colored "red" "ERROR: Port $BACKEND_PORT is already in use."
    echo_colored "yellow" "Another process is already using the default backend port."
    echo_colored "blue" "You can find and kill the process with:"
    echo_colored "blue" "  lsof -i :$BACKEND_PORT"
    echo_colored "blue" "  kill -9 \$(lsof -t -i :$BACKEND_PORT)"
    exit 1
  fi
fi

# Run both backend and frontend using concurrently
cd "$PROJECT_ROOT/frontend"
./node_modules/.bin/concurrently \
  --kill-others \
  --prefix "[{name}]" \
  --names "backend,frontend" \
  --prefix-colors "yellow.bold,cyan.bold" \
  "cd $PROJECT_ROOT/backend && poetry run uvicorn mnist.app:app --reload" \
  "npm start"
