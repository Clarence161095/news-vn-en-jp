# 🔄 RESET Script - Hướng dẫn sử dụng

## 🎯 Mục đích

Script `reset.sh` dùng để reset toàn bộ app về trạng thái sạch, giải quyết các vấn đề:
- ❌ SQLite database bị lỗi/corrupt
- ❌ Dependencies bị lỗi
- ❌ App không khởi động được
- ❌ Virtual environment bị lỗi

## ⚠️ Cảnh báo

**Script này sẽ:**
- 🛑 Stop app đang chạy
- 💾 Backup database hiện tại
- 🗑️ Xóa database cũ
- 🗑️ Xóa virtual environment
- ✨ Tạo lại tất cả từ đầu
- 🚀 Khởi động app mới

**⚠️ LƯU Ý:** Database sẽ bị xóa (nhưng đã backup). Tất cả dữ liệu trong app sẽ mất!

## 🚀 Cách sử dụng

### Cách 1: Chạy script trực tiếp

```bash
cd news-vn-en-jp
./reset.sh
```

Script sẽ hỏi xác nhận:
```
⚠️  WARNING: This will:
  - Stop running app
  - Backup current database
  - Remove and recreate database
  - Reinstall dependencies
  - Start app fresh

Continue? (y/N):
```

Nhấn `y` để tiếp tục.

### Cách 2: Chạy không cần xác nhận (auto yes)

```bash
yes | ./reset.sh
```

## 📊 Các bước script thực hiện

### Step 1: Stop running app ✅
- Tìm và stop tất cả process Gunicorn
- Kill force nếu không stop được

### Step 2: Backup existing database ✅
- Backup vào thư mục `backups/`
- Tên file: `articles_reset_backup_YYYYMMDD_HHMMSS.db`
- Cả `katakana_cache.json` cũng được backup

### Step 3: Clean old files ✅
- Xóa `articles.db`
- Xóa `articles.db-journal`, `articles.db-wal`, `articles.db-shm`
- Xóa `__pycache__/`
- Clean logs cũ

### Step 4: Check Python environment ✅
- Kiểm tra Python3 có cài chưa
- Hiển thị Python version

### Step 5: Recreate virtual environment ✅
- Xóa venv cũ (nếu có)
- Tạo venv mới
- Activate venv

### Step 6: Install dependencies ✅
- Upgrade pip
- Install từ `requirements.txt`
- Verify installation

### Step 7: Initialize database ✅
- Tạo `articles.db` mới
- Tạo table `articles`
- Tạo table `article_cache`
- Verify tables created

### Step 8: Start app in background ✅
- Start Gunicorn daemon mode
- Bind `0.0.0.0:5000`
- Logs vào `logs/access.log` và `logs/error.log`

## 📋 Output mẫu

```
🔄 FULL RESET & RESTART News App
======================================
⚠️  WARNING: This will:
  - Stop running app
  - Backup current database
  - Remove and recreate database
  - Reinstall dependencies
  - Start app fresh

Continue? (y/N): y

======================================
🔄 Starting Full Reset Process...
======================================

📍 Step 1/8: Stopping running app...
✅ App stopped

📍 Step 2/8: Backing up existing database...
✅ Database backed up to: backups/articles_reset_backup_20251122_210000.db
✅ Katakana cache backed up

📍 Step 3/8: Cleaning old files...
✅ Removed articles.db
✅ Removed __pycache__

📍 Step 4/8: Checking Python environment...
✅ Found: Python 3.10.12

📍 Step 5/8: Setting up virtual environment...
✅ Virtual environment created
✅ Virtual environment activated

📍 Step 6/8: Installing dependencies...
✅ pip upgraded
✅ Dependencies installed

📍 Step 7/8: Initializing fresh database...
Initializing database tables...
✅ Table 'articles' created
✅ Table 'article_cache' created
✅ Table 'articles' has 10 columns
✅ Table 'article_cache' has 6 columns
✅ Database initialized successfully!
✅ Database file created (size: 24K)

📍 Step 8/8: Starting app in background...
✅ App started successfully (PID: 12345)

======================================
📊 Final Status Check
======================================

✅ Process: RUNNING
   PIDs: 12345 12346 12347 12348 12349
✅ Port 5000: LISTENING
✅ Database: EXISTS (size: 24K)
   Tables: 2

Access URLs:
  Local:    http://localhost:5000
  Private:  http://172.31.45.123:5000
  Public:   http://54.123.45.67:5000

Testing local connection...
✅ HTTP Test: SUCCESS (Status: 200)

📝 Logs:
  Access:  tail -f logs/access.log
  Error:   tail -f logs/error.log

🛠️  Useful Commands:
  ./status.sh          # Check status
  ./stop.sh            # Stop app
  tail -f logs/error.log   # View error logs

======================================
🎉 Reset Complete!
======================================

✅ App is running and responding!

🌐 Access your app at: http://54.123.45.67:5000
```

## 🔍 Kiểm tra sau khi reset

### 1. Check status

```bash
./status.sh
```

Phải thấy:
- ✅ Status: RUNNING
- ✅ Port 5000: LISTENING
- ✅ Database: EXISTS

### 2. Test HTTP

```bash
curl http://localhost:5000
```

Phải trả về HTML trang chủ (không phải error).

### 3. Check logs

```bash
tail -f logs/error.log
```

Không có error nghiêm trọng.

### 4. Test từ browser

```
http://YOUR_EC2_PUBLIC_IP:5000
```

Phải hiển thị trang chủ.

## 🐛 Troubleshooting

### Script báo lỗi "Python3 not found"

```bash
# Cài Python
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Chạy lại
./reset.sh
```

### Script báo lỗi "requirements.txt not found"

```bash
# Check file có tồn tại không
ls -la requirements.txt

# Nếu không có, tạo lại
cat > requirements.txt << EOF
Flask==3.0.0
Werkzeug==3.0.1
pykakasi==2.2.1
eng-to-ipa==0.0.2
deep-translator==1.11.4
gunicorn==21.2.0
EOF

# Chạy lại
./reset.sh
```

### Database initialization failed

```bash
# Check Python có import được app không
source venv/bin/activate
python -c "from app import init_db; print('OK')"

# Nếu lỗi, check app.py có tồn tại không
ls -la app.py

# Chạy lại
./reset.sh
```

### App không start

```bash
# Check logs
tail -50 logs/error.log

# Check port có bị chiếm không
sudo lsof -i :5000

# Kill process cũ
sudo pkill -9 -f gunicorn

# Chạy lại
./reset.sh
```

### HTTP Test failed

```bash
# Wait thêm vài giây
sleep 5

# Test lại
curl http://localhost:5000

# Nếu vẫn fail, check logs
tail -f logs/error.log
```

## 💾 Restore database từ backup

Nếu cần restore database cũ:

```bash
# List backups
ls -lh backups/

# Restore
cp backups/articles_reset_backup_YYYYMMDD_HHMMSS.db articles.db

# Restart app
./stop.sh
./start-background.sh
```

## 🔄 Khi nào dùng reset.sh?

### ✅ NÊN dùng khi:
- SQLite database bị corrupt
- App không khởi động được
- Dependencies bị lỗi
- Virtual environment bị lỗi
- Sau khi update Python version
- Sau khi update dependencies lớn

### ❌ KHÔNG NÊN dùng khi:
- Chỉ cần update code → Dùng `./update.sh`
- Chỉ cần restart app → Dùng `./stop.sh && ./start-background.sh`
- Đang có dữ liệu quan trọng chưa backup

## 📊 So sánh các scripts

| Script | Mục đích | Dữ liệu |
|--------|----------|---------|
| `update.sh` | Update code từ GitHub | ✅ Giữ nguyên |
| `start-background.sh` | Start app | ✅ Giữ nguyên |
| `stop.sh` | Stop app | ✅ Giữ nguyên |
| `reset.sh` | Reset toàn bộ | ❌ Xóa (có backup) |

## 🎯 Best Practices

1. **Backup trước khi reset:**
   ```bash
   cp articles.db manual_backup_$(date +%Y%m%d).db
   ./reset.sh
   ```

2. **Check status sau reset:**
   ```bash
   ./reset.sh
   sleep 5
   ./status.sh
   curl http://localhost:5000
   ```

3. **Monitor logs:**
   ```bash
   ./reset.sh
   tail -f logs/error.log  # Trong terminal khác
   ```

## 📞 Quick Commands

```bash
# Full reset
./reset.sh

# Reset without confirm
yes | ./reset.sh

# Reset và check status
./reset.sh && sleep 5 && ./status.sh

# Reset và monitor logs
./reset.sh && tail -f logs/error.log

# Backup trước khi reset
cp articles.db backup_$(date +%Y%m%d).db && ./reset.sh
```

---

**Script này là "panic button" để reset mọi thứ về trạng thái sạch! 🔄**
