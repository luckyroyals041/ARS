#!/bin/bash
echo "Starting Automated Reporting System with network access..."

# Get the local IP address
NETWORK_IP=$(hostname -I | awk '{print $1}')
echo "Local network IP: $NETWORK_IP"

# Start backend server
echo "Starting backend server..."
cd backend
npm install &> /dev/null
node index.js &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"
cd ..

# Wait a moment for backend to initialize
sleep 2

# Start frontend server
echo "Starting frontend server..."
cd frontend
npm install &> /dev/null
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"

echo "All servers started successfully!"
echo "Backend running on http://$NETWORK_IP:5000"
echo "Frontend running on http://$NETWORK_IP:5173"
echo ""
echo "Use the following credentials to login:"
echo "Faculty: username: faculty, password: faculty123"
echo "HoD: username: hod, password: hod123"
echo "Principal: username: principal, password: principal123"
echo "Admin: username: admin, password: admin123"
echo ""
echo "To stop all servers, run: ./stop_all.sh"