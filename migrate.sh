#!/bin/bash

# ============================================
# 🚀 MIGRATE & DEPLOY SCRIPT
# Deploy latest code to EC2 without data loss
# ============================================

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$APP_DIR/backups"
LOG_DIR="$APP_DIR/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo ""
echo -e "${BLUE}======================================"
echo "🚀 MIGRATE & DEPLOY"
echo "======================================"
echo -e "${NC}"
echo "📍 App Directory: $APP_DIR"
echo "📅 Timestamp: $TIMESTAMP"
echo ""

# ============================================
# STEP 1: Pre-flight checks
# ============================================
echo -e "${YELLOW}📍 Step 1/6: Pre-flight checks...${NC}"

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Not a git repository!${NC}"
    echo "Please run this script from the project root directory."
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "   Current branch: $CURRENT_BRANCH"

# Check for local changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted local changes${NC}"
    echo ""
    git status --short
    echo ""
    read -p "Continue anyway? Local changes will be preserved. (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

echo -e "${GREEN}✅ Pre-flight checks passed${NC}"

# ============================================
# STEP 2: Backup database before migration
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 2/6: Backing up database...${NC}"

mkdir -p "$BACKUP_DIR"

if [ -f "articles.db" ]; then
    BACKUP_FILE="$BACKUP_DIR/articles_migrate_backup_$TIMESTAMP.db"
    cp articles.db "$BACKUP_FILE"
    echo -e "${GREEN}✅ Database backed up to: $BACKUP_FILE${NC}"
    
    # Show backup size
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "   Backup size: $BACKUP_SIZE"
else
    echo -e "${YELLOW}ℹ️  No existing database to backup${NC}"
fi

# ============================================
# STEP 3: Pull latest code from remote
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 3/6: Pulling latest code from remote...${NC}"

# Fetch all changes
echo "   Fetching from origin..."
git fetch origin

# Check if there are updates
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "${GREEN}✅ Already up to date!${NC}"
else
    echo "   Local:  $LOCAL"
    echo "   Remote: $REMOTE"
    echo ""
    
    # Show what will change
    echo -e "${CYAN}📋 Changes to be applied:${NC}"
    git log --oneline HEAD..origin/main | head -10
    COMMIT_COUNT=$(git log --oneline HEAD..origin/main | wc -l)
    echo "   Total: $COMMIT_COUNT new commit(s)"
    echo ""
    
    # Pull changes (merge strategy to preserve local changes)
    echo "   Pulling changes..."
    git pull origin main --no-edit
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Git pull failed!${NC}"
        echo "Please resolve conflicts manually and run again."
        exit 1
    fi
    
    echo -e "${GREEN}✅ Code updated successfully${NC}"
fi

# ============================================
# STEP 4: Stop running server
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 4/6: Stopping running server...${NC}"

# Try to stop gunicorn (production)
if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
    echo "   Stopping gunicorn..."
    pkill -f "gunicorn.*app:app"
    sleep 2
    
    # Force kill if still running
    if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
        pkill -9 -f "gunicorn.*app:app"
        sleep 1
    fi
    echo -e "${GREEN}✅ Gunicorn stopped${NC}"
fi

# Try to stop Flask dev server
if pgrep -f "python.*app.py" > /dev/null 2>&1; then
    echo "   Stopping Flask dev server..."
    pkill -f "python.*app.py"
    sleep 2
    echo -e "${GREEN}✅ Flask dev server stopped${NC}"
fi

# Check if anything was stopped
if ! pgrep -f "gunicorn.*app:app" > /dev/null 2>&1 && ! pgrep -f "python.*app.py" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ All servers stopped${NC}"
else
    echo -e "${YELLOW}ℹ️  No running server found${NC}"
fi

# ============================================
# STEP 5: Apply migrations (update dependencies & DB)
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 5/6: Applying migrations...${NC}"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "   Virtual environment activated (Linux)"
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    echo "   Virtual environment activated (Windows)"
else
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Run ./reset.sh first to set up the environment."
    exit 1
fi

# Update dependencies if requirements.txt changed
echo ""
echo "   Checking for new dependencies..."
pip install -r requirements.txt --quiet --upgrade

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies updated${NC}"
else
    echo -e "${YELLOW}⚠️  Some dependencies may have issues${NC}"
fi

# Run database migrations by importing app (this triggers init_db)
echo ""
echo "   Running database migrations..."

python << 'EOF'
import sys
try:
    # Import app to trigger init_db() which handles migrations
    from app import init_db, get_db
    
    print("   Initializing/migrating database...")
    init_db()
    
    # Verify database structure
    conn = get_db()
    cursor = conn.cursor()
    
    # Check articles table columns
    cursor.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in cursor.fetchall()]
    
    expected_columns = ['id', 'title_vi', 'title_en', 'title_jp', 'content_vi', 'content_en', 'content_jp', 'category', 'is_favorite', 'created_by', 'created_at', 'updated_at']
    
    missing = [col for col in expected_columns if col not in columns]
    if missing:
        print(f"   ⚠️  Missing columns: {missing}")
    else:
        print(f"   ✅ All {len(columns)} columns present in articles table")
    
    # Check article count
    count = cursor.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    print(f"   📊 Total articles: {count}")
    
    conn.close()
    print("   ✅ Database migration complete!")
    
except Exception as e:
    print(f"   ❌ Migration error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database migration failed!${NC}"
    echo ""
    echo "To restore from backup:"
    echo "  cp $BACKUP_FILE articles.db"
    exit 1
fi

echo -e "${GREEN}✅ Migrations applied successfully${NC}"

# ============================================
# STEP 6: Start server with new code
# ============================================
echo ""
echo -e "${YELLOW}📍 Step 6/6: Starting server...${NC}"

mkdir -p "$LOG_DIR"

# Detect environment and start appropriate server
if command -v gunicorn &> /dev/null; then
    # Production - use Gunicorn
    echo "   Starting Gunicorn (production mode)..."
    
    nohup gunicorn \
        --workers 4 \
        --bind 0.0.0.0:5000 \
        --access-logfile "$LOG_DIR/access.log" \
        --error-logfile "$LOG_DIR/error.log" \
        --log-level info \
        --daemon \
        --pid "$APP_DIR/gunicorn.pid" \
        app:app
    
    sleep 3
    
    if pgrep -f "gunicorn.*app:app" > /dev/null 2>&1; then
        PID=$(cat "$APP_DIR/gunicorn.pid" 2>/dev/null || pgrep -f "gunicorn.*app:app" | head -1)
        echo -e "${GREEN}✅ Gunicorn started (PID: $PID)${NC}"
    else
        echo -e "${RED}❌ Failed to start Gunicorn${NC}"
        tail -20 "$LOG_DIR/error.log"
        exit 1
    fi
else
    # Development - use Flask
    echo "   Starting Flask development server..."
    
    nohup python app.py > "$LOG_DIR/access.log" 2> "$LOG_DIR/error.log" &
    
    sleep 3
    echo -e "${GREEN}✅ Flask server started${NC}"
fi

# ============================================
# Final Status
# ============================================
echo ""
echo -e "${BLUE}======================================"
echo "📊 Migration Summary"
echo -e "======================================${NC}"
echo ""

# Show git status
echo -e "${CYAN}📌 Current Version:${NC}"
git log -1 --oneline
echo ""

# Test connection
echo -e "${CYAN}🔗 Testing connection...${NC}"
sleep 2
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null)

if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Server is responding (HTTP $HTTP_STATUS)${NC}"
else
    echo -e "${YELLOW}⚠️  Server returned HTTP $HTTP_STATUS${NC}"
fi

# Get access URLs
echo ""
echo -e "${CYAN}🌐 Access URLs:${NC}"
echo "   Local:   http://localhost:5000"

# Get private IP
PRIVATE_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -n "$PRIVATE_IP" ]; then
    echo "   Private: http://$PRIVATE_IP:5000"
fi

# Get public IP (EC2)
PUBLIC_IP=$(curl -s --connect-timeout 2 http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null)
if [ -n "$PUBLIC_IP" ]; then
    echo -e "${GREEN}   Public:  http://$PUBLIC_IP:5000${NC}"
fi

# Show backup info
echo ""
echo -e "${CYAN}💾 Backup:${NC}"
if [ -f "$BACKUP_FILE" ]; then
    echo "   $BACKUP_FILE"
fi

# Final message
echo ""
echo -e "${BLUE}======================================"
echo -e "${GREEN}🎉 Migration Complete!${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo -e "${YELLOW}📝 Useful commands:${NC}"
echo "   ./status.sh              # Check server status"
echo "   ./stop.sh                # Stop server"
echo "   tail -f logs/error.log   # View error logs"
echo "   tail -f logs/access.log  # View access logs"
echo ""
