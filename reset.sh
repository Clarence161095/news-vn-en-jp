#!/bin/bash

echo "🔄 FULL RESET & RESTART News App"
echo "======================================"
echo "⚠️  WARNING: This will:"
echo "  - Stop running app"
echo "  - Backup current database"
echo "  - Remove and recreate database"
echo "  - Reinstall dependencies"
echo "  - Start app fresh"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}======================================"
echo "🔄 Starting Full Reset Process..."
echo -e "======================================${NC}"
echo ""

# ============================================
# STEP 1: Stop running app
# ============================================
echo -e "${YELLOW}📍 Step 1/8: Stopping running app...${NC}"
if pgrep -f "gunicorn.*app:app" > /dev/null; then
    pkill -f "gunicorn.*app:app"
    sleep 2
    if pgrep -f "gunicorn.*app:app" > /dev/null; then
        pkill -9 -f "gunicorn.*app:app"
    fi
    echo -e "${GREEN}✅ App stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  No app running${NC}"
fi

# ============================================
# STEP 2: Backup existing database
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 2/8: Backing up existing database...${NC}"
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"

if [ -f "articles.db" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/articles_reset_backup_$TIMESTAMP.db"
    cp articles.db "$BACKUP_FILE"
    echo -e "${GREEN}✅ Database backed up to: $BACKUP_FILE${NC}"
    
    # Also backup katakana cache if exists
    if [ -f "katakana_cache.json" ]; then
        cp katakana_cache.json "$BACKUP_DIR/katakana_cache_backup_$TIMESTAMP.json"
        echo -e "${GREEN}✅ Katakana cache backed up${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  No existing database to backup${NC}"
fi

# ============================================
# STEP 3: Clean old files
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 3/8: Cleaning old files...${NC}"

# Remove database files
if [ -f "articles.db" ]; then
    rm -f articles.db
    echo -e "${GREEN}✅ Removed articles.db${NC}"
fi

if [ -f "articles.db-journal" ]; then
    rm -f articles.db-journal
    echo -e "${GREEN}✅ Removed articles.db-journal${NC}"
fi

if [ -f "articles.db-wal" ]; then
    rm -f articles.db-wal
    echo -e "${GREEN}✅ Removed articles.db-wal${NC}"
fi

if [ -f "articles.db-shm" ]; then
    rm -f articles.db-shm
    echo -e "${GREEN}✅ Removed articles.db-shm${NC}"
fi

# Clean Python cache
if [ -d "__pycache__" ]; then
    rm -rf __pycache__
    echo -e "${GREEN}✅ Removed __pycache__${NC}"
fi

# Clean old logs
if [ -d "logs" ]; then
    rm -f logs/*.log
    echo -e "${GREEN}✅ Cleaned old logs${NC}"
fi

# ============================================
# STEP 4: Check Python and pip
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 4/8: Checking Python environment...${NC}"

# Detect Python command (py on Windows, python3 on Linux)
PYTHON_CMD=""
if command -v py &> /dev/null; then
    # Windows - use py launcher
    PYTHON_CMD="py"
elif command -v python3 &> /dev/null; then
    # Linux/Mac
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Generic python
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found!${NC}"
    echo "Please install Python:"
    echo "  Linux: sudo apt update && sudo apt install python3 python3-pip python3-venv -y"
    echo "  Windows: Download from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}✅ Found: $PYTHON_VERSION (using '$PYTHON_CMD')${NC}"

# ============================================
# STEP 5: Recreate virtual environment
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 5/8: Setting up virtual environment...${NC}"

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create new venv
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment created${NC}"

# Activate venv (different paths on Windows vs Linux)
if [ -f "venv/Scripts/activate" ]; then
    # Windows
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    # Linux/Mac
    source venv/bin/activate
else
    echo -e "${RED}❌ Failed to find activation script${NC}"
    exit 1
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# ============================================
# STEP 6: Install dependencies
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 6/8: Installing dependencies...${NC}"

# Upgrade pip
pip install --upgrade pip --quiet
echo -e "${GREEN}✅ pip upgraded${NC}"

# Install requirements
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found!${NC}"
    exit 1
fi

pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Dependencies installed${NC}"

# ============================================
# STEP 7: Initialize database
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 7/8: Initializing fresh database...${NC}"

# Create a Python script to initialize DB
cat > init_db.py << 'EOF'
import sqlite3
import sys

try:
    # Import app to trigger init_db()
    from app import init_db
    
    print("Initializing database tables...")
    init_db()
    
    # Verify tables were created
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    
    # Check articles table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
    if cursor.fetchone():
        print("✅ Table 'articles' created")
    else:
        print("❌ Table 'articles' not found")
        sys.exit(1)
    
    # Check article_cache table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='article_cache'")
    if cursor.fetchone():
        print("✅ Table 'article_cache' created")
    else:
        print("❌ Table 'article_cache' not found")
        sys.exit(1)
    
    # Get table info
    cursor.execute("PRAGMA table_info(articles)")
    articles_columns = cursor.fetchall()
    print(f"✅ Table 'articles' has {len(articles_columns)} columns")
    
    cursor.execute("PRAGMA table_info(article_cache)")
    cache_columns = cursor.fetchall()
    print(f"✅ Table 'article_cache' has {len(cache_columns)} columns")
    
    conn.close()
    print("✅ Database initialized successfully!")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error initializing database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

# Run initialization
python init_db.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database initialization failed${NC}"
    rm -f init_db.py
    exit 1
fi

# Clean up
rm -f init_db.py

# Verify database file
if [ -f "articles.db" ]; then
    DB_SIZE=$(du -h articles.db | cut -f1)
    echo -e "${GREEN}✅ Database file created (size: $DB_SIZE)${NC}"
else
    echo -e "${RED}❌ Database file not created${NC}"
    exit 1
fi

# ============================================
# STEP 8: Start app in background
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 8/8: Starting app in background...${NC}"

# Create logs directory
mkdir -p logs

# Detect OS for server choice
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows - use Flask development server
    echo -e "${YELLOW}ℹ️  Detected Windows - using Flask development server${NC}"
    nohup $PYTHON_CMD app.py > logs/access.log 2> logs/error.log &
    SERVER_TYPE="flask"
else
    # Linux/Unix - use Gunicorn
    echo -e "${YELLOW}ℹ️  Detected Linux/Unix - using Gunicorn${NC}"
    nohup gunicorn \
        --workers 4 \
        --bind 0.0.0.0:5000 \
        --access-logfile logs/access.log \
        --error-logfile logs/error.log \
        --log-level info \
        --daemon \
        app:app
    SERVER_TYPE="gunicorn"
fi

# Wait for startup
sleep 3

# Check if running
if [[ "$SERVER_TYPE" == "gunicorn" ]]; then
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
else
    # Windows - just check if logs exist
    echo -e "${GREEN}✅ App starting (check logs for confirmation)${NC}"
fi

# ============================================
# Final Status Check
# ============================================
echo ""
echo -e "${BLUE}======================================"
echo "📊 Final Status Check"
echo -e "======================================${NC}"
echo ""

# Check process (skip on Windows as pgrep not available)
if [[ "$OSTYPE" != "msys" && "$OSTYPE" != "win32" ]]; then
    if pgrep -f "gunicorn.*app:app" > /dev/null; then
        echo -e "${GREEN}✅ Process: RUNNING${NC}"
        PIDS=$(pgrep -f "gunicorn.*app:app" | tr '\n' ' ')
        echo -e "   PIDs: $PIDS"
    else
        echo -e "${RED}❌ Process: NOT RUNNING${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  Process check skipped on Windows${NC}"
    echo -e "   Check Task Manager for 'python.exe' process"
fi

# Check port
echo ""
echo -e "${YELLOW}Checking port 5000...${NC}"
if command -v netstat &> /dev/null; then
    PORT_STATUS=$(netstat -tulpn 2>/dev/null | grep :5000 | head -1)
elif command -v ss &> /dev/null; then
    PORT_STATUS=$(ss -tulpn 2>/dev/null | grep :5000 | head -1)
fi

if [ -n "$PORT_STATUS" ]; then
    echo -e "${GREEN}✅ Port 5000: LISTENING${NC}"
else
    echo -e "${YELLOW}⚠️  Port status: Unknown (may need sudo)${NC}"
fi

# Check database
echo ""
echo -e "${YELLOW}Checking database...${NC}"
if [ -f "articles.db" ]; then
    DB_SIZE=$(du -h articles.db | cut -f1)
    echo -e "${GREEN}✅ Database: EXISTS (size: $DB_SIZE)${NC}"
    
    # Quick DB check
    TABLE_COUNT=$(sqlite3 articles.db "SELECT count(*) FROM sqlite_master WHERE type='table'" 2>/dev/null || echo "0")
    echo -e "   Tables: $TABLE_COUNT"
else
    echo -e "${RED}❌ Database: NOT FOUND${NC}"
fi

# Get IPs
echo ""
echo -e "${YELLOW}Access URLs:${NC}"
echo "  Local:    http://localhost:5000"

PRIVATE_IP=$(hostname -I | awk '{print $1}')
if [ -n "$PRIVATE_IP" ]; then
    echo "  Private:  http://$PRIVATE_IP:5000"
fi

PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
if [ -n "$PUBLIC_IP" ]; then
    echo -e "${GREEN}  Public:   http://$PUBLIC_IP:5000${NC}"
fi

# Test local connection
echo ""
echo -e "${YELLOW}Testing local connection...${NC}"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null)
if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ HTTP Test: SUCCESS (Status: $HTTP_STATUS)${NC}"
elif [ "$HTTP_STATUS" = "000" ]; then
    echo -e "${RED}❌ HTTP Test: FAILED (Connection refused)${NC}"
else
    echo -e "${YELLOW}⚠️  HTTP Test: Status $HTTP_STATUS${NC}"
fi

# Show logs location
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo "  Access:  tail -f logs/access.log"
echo "  Error:   tail -f logs/error.log"

# Show commands
echo ""
echo -e "${YELLOW}🛠️  Useful Commands:${NC}"
echo "  ./status.sh          # Check status"
echo "  ./stop.sh            # Stop app"
echo "  tail -f logs/error.log   # View error logs"

# Final summary
echo ""
echo -e "${BLUE}======================================"
echo "🎉 Reset Complete!"
echo -e "======================================${NC}"
echo ""

if pgrep -f "gunicorn.*app:app" > /dev/null && [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ App is running and responding!${NC}"
    echo ""
    if [ -n "$PUBLIC_IP" ]; then
        echo -e "${GREEN}🌐 Access your app at: http://$PUBLIC_IP:5000${NC}"
    else
        echo -e "${GREEN}🌐 Access your app at: http://$PRIVATE_IP:5000${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  App may not be fully ready yet.${NC}"
    echo "Check logs with: tail -f logs/error.log"
fi

echo ""
