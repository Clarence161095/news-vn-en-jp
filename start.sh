#!/bin/bash

echo "🚀 Starting News App..."
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

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    echo "Please run deploy.sh first"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Start Gunicorn
echo -e "${YELLOW}🚀 Starting Gunicorn server...${NC}"
echo ""
echo -e "${GREEN}Server will start at: http://0.0.0.0:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
