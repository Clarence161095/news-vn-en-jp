#!/bin/bash

echo "🚀 Starting News App in Background..."
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py not found!${NC}"
    echo "Please run this script from the news-vn-en-jp directory"
    exit 1
fi

# Check if app is already running
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo -e "${YELLOW}⚠️  App is already running!${NC}"
    echo ""
    echo "To stop it, run:"
    echo "  pkill -f 'gunicorn.*app:app'"
    echo ""
    echo "Or use:"
    echo "  ./stop.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    echo "Please run deploy.sh first"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Create logs directory if not exists
mkdir -p logs

# Start Gunicorn in background
echo -e "${YELLOW}🚀 Starting Gunicorn server in background...${NC}"
nohup gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --daemon \
    app:app

# Wait a moment for the process to start
sleep 2

# Check if process is running
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    PID=$(pgrep -f "gunicorn.*app:app" | head -1)
    echo ""
    echo -e "${GREEN}🎉 App started successfully!${NC}"
    echo "======================================"
    echo ""
    echo -e "${GREEN}✅ Process ID: $PID${NC}"
    echo -e "${GREEN}✅ Listening on: 0.0.0.0:5000${NC}"
    echo ""
    echo -e "${YELLOW}📊 Access URLs:${NC}"
    echo "  Local:    http://localhost:5000"
    echo "  Network:  http://$(hostname -I | awk '{print $1}'):5000"
    if [ -n "$PUBLIC_IP" ]; then
        echo "  Public:   http://$PUBLIC_IP:5000"
    fi
    echo ""
    echo -e "${YELLOW}📝 Logs:${NC}"
    echo "  Access:   tail -f logs/access.log"
    echo "  Error:    tail -f logs/error.log"
    echo ""
    echo -e "${YELLOW}🛑 To stop:${NC}"
    echo "  ./stop.sh"
    echo "  or: pkill -f 'gunicorn.*app:app'"
    echo ""
else
    echo -e "${RED}❌ Failed to start app${NC}"
    echo "Check logs/error.log for details"
    exit 1
fi
