#!/bin/bash

# Update project files to support multiple PDF template styles
echo "Updating project files for multiple PDF template styles..."

# Create a placeholder header image
echo "Creating placeholder header image..."
mkdir -p templates/images
touch templates/images/header.png

# Update backend files
echo "Updating backend files..."
cp reports/generate_pdf_with_styles.py reports/generate_pdf.py

# Update frontend files
echo "Updating frontend files..."
cp frontend/src/pages/StudentTable_updated.jsx frontend/src/pages/StudentTable.jsx
cp frontend/src/pages/ReportDialog_updated.jsx frontend/src/pages/ReportDialog.jsx
cp frontend/src/services/api_updated.js frontend/src/services/api.js

echo "✅ Project updated successfully!"
echo ""
echo "To test the changes:"
echo "1. Start the backend server: ./run_backend.sh"
echo "2. Start the frontend server: ./run_frontend.sh"
echo "3. Generate a PDF report with your preferred template style"
echo ""
echo "Note: You should replace the placeholder header image at templates/images/header.png with your actual header image."