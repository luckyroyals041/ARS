#!/bin/bash
echo "Starting Automated Reporting System..."
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
echo "Backend running on http://0.0.0.0:5000"
NETWORK_IP=$(hostname -I | awk '{print $1}')
echo "Frontend running on http://$NETWORK_IP:5173"
echo ""
echo "Use the following credentials to login:"
echo "Faculty: username: faculty, password: faculty123"
echo ""
echo "To stop all servers, run: ./stop_all.sh"