#!/bin/bash

# Activate virtual environment
source provenv/bin/activate

# Navigate to frontend directory
cd frontend

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start the development server
echo "Starting frontend development server..."
npm run dev