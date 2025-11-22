#!/bin/bash

echo "📊 News App Status"
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if app is running
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo -e "${GREEN}✅ Status: RUNNING${NC}"
    echo ""
    
    # Get process details
    echo -e "${YELLOW}Process Details:${NC}"
    ps aux | grep "gunicorn.*app:app" | grep -v grep
    echo ""
    
    # Get PIDs
    PIDS=$(pgrep -f "gunicorn.*app:app")
    echo -e "${YELLOW}PIDs: $PIDS${NC}"
    echo ""
    
    # Check port
    echo -e "${YELLOW}Port Status:${NC}"
    if command -v netstat &> /dev/null; then
        netstat -tulpn 2>/dev/null | grep :5000 || echo "Port 5000 not found (may need sudo)"
    elif command -v ss &> /dev/null; then
        ss -tulpn 2>/dev/null | grep :5000 || echo "Port 5000 not found (may need sudo)"
    fi
    echo ""
    
    # Access URLs
    echo -e "${YELLOW}Access URLs:${NC}"
    echo "  Local:    http://localhost:5000"
    PRIVATE_IP=$(hostname -I | awk '{print $1}')
    if [ -n "$PRIVATE_IP" ]; then
        echo "  Private:  http://$PRIVATE_IP:5000"
    fi
    
    # Try to get public IP (EC2)
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
    if [ -n "$PUBLIC_IP" ]; then
        echo -e "${GREEN}  Public:   http://$PUBLIC_IP:5000${NC}"
    fi
    echo ""
    
    # Logs
    echo -e "${YELLOW}Recent Logs (last 5 lines):${NC}"
    if [ -f "logs/error.log" ]; then
        echo "Error log:"
        tail -5 logs/error.log
    fi
    echo ""
    
else
    echo -e "${RED}❌ Status: NOT RUNNING${NC}"
    echo ""
    echo "To start the app:"
    echo "  ./start-background.sh   # Run in background"
    echo "  ./start.sh              # Run in foreground"
fi

echo ""
echo -e "${YELLOW}Available Commands:${NC}"
echo "  ./start-background.sh   # Start in background"
echo "  ./stop.sh               # Stop app"
echo "  ./status.sh             # This status check"
echo "  tail -f logs/error.log  # View error logs"
echo "  tail -f logs/access.log # View access logs"
