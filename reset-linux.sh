#!/bin/bash

# ============================================
# FULL RESET & RESTART - Linux/EC2 Version
# ============================================
# This script completely resets the News App:
# - Stops running app
# - Backs up database
# - Removes and recreates database
# - Reinstalls all dependencies
# - Starts app fresh on 0.0.0.0:5000
# ============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================
# Confirmation Prompt
# ============================================
echo -e "${BLUE}🔄 FULL RESET & RESTART News App${NC}"
echo "======================================"
echo -e "${YELLOW}⚠️  WARNING: This will:${NC}"
echo "  - Stop running app"
echo "  - Backup current database"
echo "  - Remove and recreate database"
echo "  - Reinstall dependencies"
echo "  - Start app fresh"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# ============================================
# Start Reset Process
# ============================================
echo ""
echo -e "${BLUE}======================================"
echo "🔄 Starting Full Reset Process..."
echo -e "======================================${NC}"
echo ""

# ============================================
# STEP 1: Stop Running App
# ============================================
echo -e "${YELLOW}📍 Step 1/8: Stopping running app...${NC}"

if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
    pkill -f "gunicorn.*app:app" || true
    sleep 2
    if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
        pkill -9 -f "gunicorn.*app:app" || true
    fi
    echo -e "${GREEN}✅ App stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  No app running${NC}"
fi

echo ""

# ============================================
# STEP 2: Backup Database
# ============================================
echo -e "${YELLOW}📍 Step 2/8: Backing up existing database...${NC}"

mkdir -p backups

if [ -f "articles.db" ]; then
    BACKUP_FILE="backups/articles_reset_backup_$(date +%Y%m%d_%H%M%S).db"
    cp articles.db "$BACKUP_FILE"
    echo -e "${GREEN}✅ Database backed up to: $BACKUP_FILE${NC}"
    
    # Also backup katakana cache if exists
    if [ -f "katakana_cache.json" ]; then
        cp katakana_cache.json "backups/katakana_cache_backup_$(date +%Y%m%d_%H%M%S).json"
        echo -e "${GREEN}✅ Katakana cache backed up${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  No existing database to backup${NC}"
fi

echo ""

# ============================================
# STEP 3: Clean Old Files
# ============================================
echo -e "${YELLOW}📍 Step 3/8: Cleaning old files...${NC}"

# Remove database
if [ -f "articles.db" ]; then
    rm articles.db
    echo -e "${GREEN}✅ Removed articles.db${NC}"
fi

# Clean Python cache
if [ -d "__pycache__" ]; then
    rm -rf __pycache__
    echo -e "${GREEN}✅ Removed __pycache__${NC}"
fi

find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Clean old logs
if [ -d "logs" ]; then
    rm -f logs/*.log
    echo -e "${GREEN}✅ Cleaned old logs${NC}"
fi

echo ""

# ============================================
# STEP 4: Check Python Environment
# ============================================
echo -e "${YELLOW}📍 Step 4/8: Checking Python environment...${NC}"

# Detect Python command
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found!${NC}"
    echo "Please install Python 3.8+ first:"
    echo "  sudo yum install python3  # Amazon Linux 2"
    echo "  sudo apt install python3  # Ubuntu/Debian"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}✅ Found: $PYTHON_VERSION (using '$PYTHON_CMD')${NC}"

echo ""

# ============================================
# STEP 5: Setup Virtual Environment
# ============================================
echo -e "${YELLOW}📍 Step 5/8: Setting up virtual environment...${NC}"

# Remove old venv
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create new venv
$PYTHON_CMD -m venv venv
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate venv
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

echo ""

# ============================================
# STEP 6: Install Dependencies
# ============================================
echo -e "${YELLOW}📍 Step 6/8: Installing dependencies...${NC}"

# Upgrade pip
pip install --upgrade pip --quiet
echo -e "${GREEN}✅ pip upgraded${NC}"

# Install requirements
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

echo ""

# ============================================
# STEP 7: Initialize Database
# ============================================
echo -e "${YELLOW}📍 Step 7/8: Initializing fresh database...${NC}"

# Create temporary init script
cat > init_db.py << 'EOFPYTHON'
from app import init_db
import os

print("Initializing database tables...")
init_db()

# Verify database was created
if os.path.exists('articles.db'):
    import sqlite3
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        print(f"✅ Table '{table[0]}' created")
        
        # Count columns
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"✅ Table '{table[0]}' has {len(columns)} columns")
    
    conn.close()
    print("✅ Database initialized successfully!")
else:
    print("❌ Database file not created!")
    exit(1)
EOFPYTHON

# Run init script
python init_db.py

# Clean up
rm init_db.py

# Verify database file
if [ -f "articles.db" ]; then
    DB_SIZE=$(du -h articles.db | cut -f1)
    echo -e "${GREEN}✅ Database file created (size: $DB_SIZE)${NC}"
else
    echo -e "${RED}❌ Database initialization failed${NC}"
    exit 1
fi

echo ""

# ============================================
# STEP 8: Start App
# ============================================
echo -e "${YELLOW}📍 Step 8/8: Starting app in background...${NC}"

# Create logs directory
mkdir -p logs

# Start Gunicorn on 0.0.0.0:5000
nohup gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --daemon \
    app:app

# Wait for startup
sleep 3

# Check if running
if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
    PID=$(pgrep -f "gunicorn.*app:app" | head -1)
    echo -e "${GREEN}✅ App started successfully (PID: $PID)${NC}"
else
    echo -e "${RED}❌ Failed to start app${NC}"
    echo "Check logs/error.log for details:"
    if [ -f "logs/error.log" ]; then
        tail -20 logs/error.log
    fi
    exit 1
fi

# ============================================
# Final Status Check
# ============================================
echo ""
echo -e "${BLUE}======================================"
echo "📊 Final Status Check"
echo -e "======================================${NC}"
echo ""

# Check process
if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Process: RUNNING${NC}"
    PIDS=$(pgrep -f "gunicorn.*app:app" | tr '\n' ' ')
    echo -e "   PIDs: $PIDS"
else
    echo -e "${RED}❌ Process: NOT RUNNING${NC}"
fi

# Check port
echo ""
echo "Checking port 5000..."
if command -v netstat &> /dev/null; then
    if netstat -tuln | grep -q ":5000 "; then
        echo -e "${GREEN}✅ Port 5000: LISTENING${NC}"
    else
        echo -e "${RED}❌ Port 5000: NOT LISTENING${NC}"
    fi
elif command -v ss &> /dev/null; then
    if ss -tuln | grep -q ":5000 "; then
        echo -e "${GREEN}✅ Port 5000: LISTENING${NC}"
    else
        echo -e "${RED}❌ Port 5000: NOT LISTENING${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Port status: Unknown (netstat/ss not found)${NC}"
fi

# Check database
echo ""
echo "Checking database..."
if [ -f "articles.db" ]; then
    DB_SIZE=$(du -h articles.db | cut -f1)
    
    # Count articles
    ARTICLE_COUNT=$(sqlite3 articles.db "SELECT COUNT(*) FROM articles" 2>/dev/null || echo "0")
    
    echo -e "${GREEN}✅ Database: EXISTS (size: $DB_SIZE)${NC}"
    echo -e "   Articles: $ARTICLE_COUNT"
else
    echo -e "${RED}❌ Database: NOT FOUND${NC}"
fi

# Get server info
echo ""
echo "Access URLs:"

# Local IP
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "127.0.0.1")
echo -e "  Local:    http://localhost:5000"
echo -e "  Network:  http://$LOCAL_IP:5000"

# Try to get public IP (EC2)
if command -v curl &> /dev/null; then
    PUBLIC_IP=$(curl -s --max-time 2 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "")
    if [ -n "$PUBLIC_IP" ]; then
        echo -e "  ${GREEN}Public:   http://$PUBLIC_IP:5000${NC}"
        echo -e "  ${YELLOW}⚠️  Make sure Security Group allows port 5000${NC}"
    fi
fi

# Test local connection
echo ""
echo "Testing local connection..."
if curl -s --max-time 5 http://localhost:5000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ HTTP Test: SUCCESS${NC}"
else
    echo -e "${YELLOW}⚠️  HTTP Test: App may still be starting...${NC}"
    echo "   Wait 10 seconds and try: curl http://localhost:5000"
fi

# ============================================
# Final Instructions
# ============================================
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo "  Access:  tail -f logs/access.log"
echo "  Error:   tail -f logs/error.log"
echo ""
echo -e "${YELLOW}🛠️  Useful Commands:${NC}"
echo "  ./status.sh          # Check status"
echo "  ./stop.sh            # Stop app"
echo "  tail -f logs/error.log   # View error logs"
echo ""

# ============================================
# Success!
# ============================================
echo -e "${BLUE}======================================"
echo "🎉 Reset Complete!"
echo -e "======================================${NC}"
echo ""

# Final check
if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ App is running and ready!${NC}"
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠️  App may not be fully ready yet.${NC}"
    echo "Check logs with: tail -f logs/error.log"
    echo ""
    exit 1
fi
