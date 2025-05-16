#!/bin/bash

echo "Setting up database for Automated Reporting System..."

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Please install MySQL first."
    exit 1
fi

# Ask for MySQL credentials
read -p "Enter MySQL username: " DB_USER
read -s -p "Enter MySQL password: " DB_PASSWORD
echo ""

# Create database and tables
echo "Creating database and tables..."
mysql -u "$DB_USER" -p"$DB_PASSWORD" < backend/db_setup.sql

if [ $? -eq 0 ]; then
    echo "✅ Database setup completed successfully!"
    
    # Update .env file with database credentials
    echo "Updating .env file..."
    cat > backend/.env << EOF
PORT=5000
DB_HOST=localhost
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_NAME=reporting_system
JWT_SECRET=your-secret-key
JWT_REFRESH_SECRET=your-refresh-secret-key
EOF
    
    echo "✅ Environment configuration updated!"
    echo ""
    echo "You can now start the backend server with: cd backend && npm start"
    echo "And the frontend with: cd frontend && npm run dev"
else
    echo "❌ Database setup failed. Please check your MySQL credentials and try again."
fi