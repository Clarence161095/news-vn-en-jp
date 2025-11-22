#!/bin/bash

echo "🚀 Starting deployment of News App..."
echo "======================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Clone repository
echo -e "${YELLOW}📥 Step 1: Cloning repository...${NC}"
if [ -d "news-vn-en-jp" ]; then
    echo -e "${RED}⚠️  Directory 'news-vn-en-jp' already exists!${NC}"
    echo "Please remove it or use update.sh instead"
    exit 1
fi

git clone https://github.com/Clarence161095/news-vn-en-jp.git
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to clone repository${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Repository cloned successfully${NC}"

# Step 2: Navigate to directory
cd news-vn-en-jp

# Step 3: Create virtual environment
echo -e "${YELLOW}📦 Step 2: Creating virtual environment...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Step 4: Activate virtual environment
echo -e "${YELLOW}🔄 Step 3: Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Step 5: Install dependencies
echo -e "${YELLOW}📚 Step 4: Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies installed successfully${NC}"

# Step 6: Start Gunicorn
echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo "======================================"
echo ""
echo -e "${YELLOW}To start the app, run:${NC}"
echo "cd news-vn-en-jp"
echo "source venv/bin/activate"
echo "gunicorn --workers 4 --bind 0.0.0.0:5000 app:app"
echo ""
echo -e "${YELLOW}Or start in background with:${NC}"
echo "nohup gunicorn --workers 4 --bind 0.0.0.0:5000 app:app > app.log 2>&1 &"
echo ""
echo -e "${GREEN}Access the app at: http://localhost:5000${NC}"
