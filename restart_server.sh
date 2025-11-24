#!/bin/bash

echo "🔄 Restarting Flask Server..."
echo "======================================"

cd "d:/01. Project/news-vn-en-jp"

# Kill all Python processes running app.py
echo "🛑 Stopping existing server..."
ps aux | grep "python.*app.py" | grep -v grep | awk '{print $2}' | while read pid; do
    kill -9 $pid 2>/dev/null
    echo "  Killed process $pid"
done

# Wait for processes to die
sleep 2

# Clear Python cache
echo "🧹 Clearing Python cache..."
rm -rf __pycache__
rm -f app.pyc

# Start server with venv
echo "🚀 Starting server..."
source venv/Scripts/activate
nohup python app.py > logs/access.log 2> logs/error.log &

# Get PID
sleep 2
NEW_PID=$(ps aux | grep "python.*app.py" | grep -v grep | awk '{print $2}' | head -1)

if [ -n "$NEW_PID" ]; then
    echo "✅ Server started successfully (PID: $NEW_PID)"
    echo "📡 Server running at: http://localhost:5000"
    echo ""
    echo "To view logs:"
    echo "  tail -f logs/error.log"
else
    echo "❌ Failed to start server"
    exit 1
fi
