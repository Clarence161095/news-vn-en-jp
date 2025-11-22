#!/bin/bash

echo "🛑 Stopping News App..."
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if app is running
if ! pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo -e "${YELLOW}ℹ️  App is not running${NC}"
    exit 0
fi

# Get PIDs
PIDS=$(pgrep -f "gunicorn.*app:app")
echo -e "${YELLOW}Found processes: $PIDS${NC}"

# Kill processes
echo -e "${YELLOW}Stopping Gunicorn processes...${NC}"
pkill -f "gunicorn.*app:app"

# Wait a moment
sleep 2

# Check if stopped
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo -e "${RED}⚠️  Some processes still running. Force killing...${NC}"
    pkill -9 -f "gunicorn.*app:app"
    sleep 1
fi

# Final check
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    echo -e "${RED}❌ Failed to stop app${NC}"
    exit 1
else
    echo -e "${GREEN}✅ App stopped successfully${NC}"
fi
