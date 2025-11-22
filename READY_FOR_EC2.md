# ✅ SUMMARY - Ready for EC2 Deployment

## 📦 Đã tạo/sửa các file sau:

### 1. **reset-linux.sh** ⭐ (MAIN SCRIPT)
- Script reset hoàn toàn cho EC2
- 459 dòng, 8 bước tự động
- Sử dụng Gunicorn production server
- Bind 0.0.0.0:5000 (accessible từ bên ngoài)
- ✅ Ready to use on EC2

### 2. **EC2_RESET_GUIDE.md** 📖
- Hướng dẫn chi tiết cách dùng script
- Troubleshooting guide
- Use cases và examples
- 263 dòng documentation

### 3. **RESET_QUICK_START.md** ⚡
- Quick reference ngắn gọn
- Copy-paste commands
- 40 dòng

### 4. **DEPLOYMENT_CHECKLIST.md** ✅
- Checklist deployment
- Files summary
- Testing results
- Commit commands
- 241 dòng

### 5. **app.py** (Modified)
- Thêm UTF-8 support cho Windows console
- Fix Unicode print errors
- Lines 1-13: Encoding fix

### 6. **reset.sh** (Modified)
- Cross-platform support
- Windows: Flask dev server
- Linux: Gunicorn
- Auto-detect OS và Python command

---

## 🚀 Cách deploy lên EC2:

### Bước 1: Commit và push (trên local hoặc EC2)

```bash
cd "d:\01. Project\news-vn-en-jp"

# Add files
git add reset-linux.sh EC2_RESET_GUIDE.md RESET_QUICK_START.md DEPLOYMENT_CHECKLIST.md app.py reset.sh

# Commit
git commit -m "Add EC2 reset script for database/dependency fixes"

# Push
git push origin main
```

### Bước 2: Trên EC2

```bash
# SSH vào EC2
ssh -i your-key.pem ec2-user@your-ec2-ip

# Di chuyển vào project
cd news-vn-en-jp

# Pull code mới
git pull origin main

# Make executable
chmod +x reset-linux.sh

# Chạy reset
./reset-linux.sh
# Nhấn 'y' để confirm
```

### Bước 3: Verify

```bash
# Check status
./status.sh

# Test local
curl http://localhost:5000

# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

### Bước 4: Truy cập từ browser

```
http://YOUR_EC2_PUBLIC_IP:5000
```

---

## 🎯 Script sẽ làm gì?

### 8 bước tự động:

1. ⏹️  **Stop app** - Dừng Gunicorn đang chạy
2. 💾 **Backup DB** - Sao lưu vào `backups/`
3. 🧹 **Clean files** - Xóa DB cũ, cache, logs
4. 🐍 **Check Python** - Detect Python 3
5. 📦 **Setup venv** - Tạo virtual environment mới
6. ⬇️  **Install deps** - Cài đặt lại requirements.txt
7. 🗄️  **Init database** - Tạo DB mới với đúng schema
8. 🚀 **Start app** - Khởi động Gunicorn 0.0.0.0:5000

### Thời gian: ~2-3 phút

---

## ✅ Expected Output:

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
✅ Database backed up to: backups/articles_reset_backup_20241122_230312.db

📍 Step 3/8: Cleaning old files...
✅ Removed articles.db
✅ Removed __pycache__
✅ Cleaned old logs

📍 Step 4/8: Checking Python environment...
✅ Found: Python 3.9.16 (using 'python3')

📍 Step 5/8: Setting up virtual environment...
✅ Virtual environment created
✅ Virtual environment activated

📍 Step 6/8: Installing dependencies...
✅ pip upgraded
✅ Dependencies installed

📍 Step 7/8: Initializing fresh database...
✅ Table 'articles' created
✅ Table 'article_cache' created
✅ Database initialized successfully!
✅ Database file created (size: 16K)

📍 Step 8/8: Starting app in background...
✅ App started successfully (PID: 12345)

======================================
📊 Final Status Check
======================================

✅ Process: RUNNING
   PIDs: 12345 12346 12347 12348 12349

✅ Port 5000: LISTENING

✅ Database: EXISTS (size: 16K)
   Articles: 0

Access URLs:
  Local:    http://localhost:5000
  Network:  http://10.0.1.123:5000
  Public:   http://54.123.45.67:5000
  ⚠️  Make sure Security Group allows port 5000

✅ HTTP Test: SUCCESS

======================================
🎉 Reset Complete!
======================================

✅ App is running and ready!
```

---

## ⚠️ Important Notes:

### 1. Database sẽ trống sau reset
- Tất cả articles bị xóa
- Backup tự động trong `backups/`
- Restore nếu cần: `cp backups/latest.db articles.db`

### 2. Security Group
- **Phải mở port 5000** trong AWS Security Group
- Inbound rule: TCP port 5000 from 0.0.0.0/0 (hoặc your IP)

### 3. App bind 0.0.0.0:5000
- Cho phép truy cập từ public IP
- Bắt buộc cho EC2
- Khác với 127.0.0.1 (chỉ localhost)

---

## 🔧 Troubleshooting:

### Nếu HTTP test FAILED:
```bash
# Đợi 10s cho app khởi động
sleep 10
curl http://localhost:5000

# Check logs
tail -f logs/error.log
```

### Nếu không truy cập được từ browser:
1. Check Security Group có mở port 5000
2. Check app đang chạy: `./status.sh`
3. Check public IP: `curl http://169.254.169.254/latest/meta-data/public-ipv4`

### Nếu Python not found:
```bash
# Amazon Linux 2
sudo yum install python3 -y

# Ubuntu
sudo apt install python3 python3-venv -y
```

---

## 📝 Useful Commands After Reset:

```bash
# Check app status
./status.sh

# Stop app
./stop.sh

# View real-time logs
tail -f logs/error.log
tail -f logs/access.log

# List backups
ls -lh backups/

# Restart app
./start-background.sh
```

---

## 📚 Documentation Files:

1. **RESET_QUICK_START.md** - Quick commands (START HERE)
2. **EC2_RESET_GUIDE.md** - Full documentation
3. **DEPLOYMENT_CHECKLIST.md** - This file
4. **EC2_QUICK_START.md** - Original EC2 deployment guide
5. **SCRIPTS_GUIDE.md** - All scripts usage

---

## ✨ Features:

- ✅ One-command full reset
- ✅ Automatic database backup
- ✅ Safe cleanup (no data loss with backup)
- ✅ Fresh dependency install
- ✅ Database schema verification
- ✅ Process/port/HTTP checks
- ✅ EC2 public IP detection
- ✅ Comprehensive error messages
- ✅ Production-ready (Gunicorn)
- ✅ Background mode (daemon)

---

## 🎯 Use Cases:

### ✅ Khi nào dùng reset-linux.sh:

1. SQLite database errors
2. Dependency conflicts
3. App crashes/won't start
4. After major code changes
5. Cache corruption
6. Need fresh environment

### ❌ Khi nào KHÔNG nên dùng:

1. App đang chạy tốt
2. Chỉ cần update code (dùng `update.sh`)
3. Chỉ cần restart (dùng `./stop.sh` và `./start-background.sh`)

---

## 🎉 Ready to Deploy!

**Tất cả files đã sẵn sàng. Bây giờ chỉ cần:**

1. ✅ Commit files mới
2. ✅ Push to GitHub
3. ✅ Pull trên EC2
4. ✅ Run `./reset-linux.sh`

**Good luck!** 🚀

---

**Created**: November 22, 2024
**Tested**: Windows (development) ✅
**Ready for**: EC2/Linux (production) ✅
