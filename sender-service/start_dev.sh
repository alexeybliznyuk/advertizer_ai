#!/bin/bash

# Development startup script for sender-service

echo "Starting sender-service in development mode..."

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install it first."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Create database tables
echo "Creating database tables..."
poetry run python -c "
from repository.database import create_tables
create_tables()
print('Database tables created successfully!')
"

# Start the service
echo "Starting the service..."
poetry run python main.py 