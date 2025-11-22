#!/bin/bash

echo "🔄 Updating News App..."
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

# Step 1: Stop running app (if using systemd)
echo -e "${YELLOW}🛑 Step 1: Stopping app (if running as service)...${NC}"
if systemctl is-active --quiet newsapp; then
    sudo systemctl stop newsapp
    echo -e "${GREEN}✅ Service stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  Service not running or not installed${NC}"
fi

# Step 2: Backup database
echo -e "${YELLOW}💾 Step 2: Backing up database...${NC}"
if [ -f "articles.db" ]; then
    BACKUP_DIR="backups"
    mkdir -p $BACKUP_DIR
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    cp articles.db "$BACKUP_DIR/articles_backup_$TIMESTAMP.db"
    echo -e "${GREEN}✅ Database backed up to $BACKUP_DIR/articles_backup_$TIMESTAMP.db${NC}"
else
    echo -e "${YELLOW}ℹ️  No database found to backup${NC}"
fi

# Step 3: Pull latest code
echo -e "${YELLOW}📥 Step 3: Pulling latest code...${NC}"
git pull origin develop
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to pull latest code${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Code updated successfully${NC}"

# Step 4: Activate virtual environment
echo -e "${YELLOW}🔄 Step 4: Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Step 5: Update dependencies
echo -e "${YELLOW}📚 Step 5: Updating dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt --upgrade
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to update dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies updated${NC}"

# Step 6: Restart service or show manual start command
echo ""
echo -e "${GREEN}🎉 Update completed successfully!${NC}"
echo "======================================"
echo ""

if systemctl is-enabled --quiet newsapp 2>/dev/null; then
    echo -e "${YELLOW}🔄 Restarting service...${NC}"
    sudo systemctl restart newsapp
    sudo systemctl status newsapp --no-pager
    echo ""
    echo -e "${GREEN}✅ Service restarted${NC}"
else
    echo -e "${YELLOW}To start the app, run:${NC}"
    echo "gunicorn --workers 4 --bind 0.0.0.0:5000 app:app"
    echo ""
    echo -e "${YELLOW}Or start in background:${NC}"
    echo "nohup gunicorn --workers 4 --bind 0.0.0.0:5000 app:app > app.log 2>&1 &"
fi

echo ""
echo -e "${GREEN}📊 View logs with:${NC}"
echo "tail -f app.log  # If running in background"
echo "sudo journalctl -u newsapp -f  # If running as service"
