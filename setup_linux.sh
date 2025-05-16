#!/bin/bash

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y ghostscript python3-pip python3-venv

# Create and activate virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv provenv
source provenv/bin/activate

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Set up database
echo "Setting up database..."
python database/setup_db.py

# Insert sample data
echo "Inserting sample data..."
python -c "from utils.insert_sample_data import insert_sample_data; insert_sample_data()"

echo "Setup complete! You can now run the application."