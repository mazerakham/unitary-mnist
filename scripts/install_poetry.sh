#!/bin/bash

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

echo_colored "yellow" "Attempting to install Poetry..."

# Check if we're on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo_colored "blue" "Detected macOS system. Checking for SSL certificates..."
  
  # Check if certifi is installed
  if ! python3 -c "import certifi" &> /dev/null; then
    echo_colored "yellow" "Installing certifi package for SSL certificate verification..."
    pip install certifi
  fi
  
  # Create a temporary Python script to handle SSL certificate verification
  TEMP_SCRIPT=$(mktemp)
  cat > "$TEMP_SCRIPT" << 'EOF'
import os
import sys
import subprocess
import ssl
import certifi

# Use certifi's certificate bundle
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# Run the Poetry installer
result = subprocess.run(
    ["curl", "-sSL", "https://install.python-poetry.org"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"Failed to download Poetry installer: {result.stderr}", file=sys.stderr)
    sys.exit(1)

# Pipe the installer to Python
install_process = subprocess.run(
    [sys.executable, "-"],
    input=result.stdout,
    text=True
)

sys.exit(install_process.returncode)
EOF
  
  # Run the temporary script
  python3 "$TEMP_SCRIPT"
  rm "$TEMP_SCRIPT"
else
  # Non-macOS systems can use the standard installation
  curl -sSL https://install.python-poetry.org | python3 -
fi

# Add Poetry to PATH for this session
export PATH="$HOME/.local/bin:$PATH"

# Check if installation was successful
if ! command -v poetry &> /dev/null; then
  echo_colored "red" "Failed to install Poetry automatically."
  echo_colored "red" "Please follow the manual installation instructions:"
  
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo_colored "blue" "For macOS:"
    echo_colored "blue" "1. Open Finder and navigate to /Applications/Python 3.x/"
    echo_colored "blue" "2. Double-click on 'Install Certificates.command'"
    echo_colored "blue" "3. Then run: curl -sSL https://install.python-poetry.org | python3 -"
  else
    echo_colored "blue" "curl -sSL https://install.python-poetry.org | python3 -"
  fi
  
  exit 1
else
  echo_colored "green" "Poetry installed successfully!"
fi
