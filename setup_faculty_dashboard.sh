#!/bin/bash

# Script to set up the Faculty Dashboard database

echo "Setting up Faculty Dashboard database..."

# Navigate to the backend directory
cd "$(dirname "$0")/backend"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js and try again."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Run the setup script
echo "Running database setup script..."
node scripts/setup_dashboard_db.js

echo "✅ Setup complete!"