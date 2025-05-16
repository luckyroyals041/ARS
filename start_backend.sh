#!/bin/bash

echo "Starting Automated Reporting System Backend..."

# Navigate to backend directory
cd backend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Start the backend server
echo "Starting backend server..."
node index.js

echo "Backend server started on http://localhost:5000"