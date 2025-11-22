# 📚 Script Deployment - Hướng dẫn sử dụng

## 🎯 Tổng quan

Repository này có 4 scripts giúp deploy và quản lý app dễ dàng:

| Script | Mục đích | Khi nào dùng |
|--------|----------|--------------|
| `deploy.sh` | Deploy lần đầu | Lần đầu tiên cài đặt app |
| `update.sh` | Update source code | Khi có code mới từ GitHub |
| `start.sh` | Start app | Khởi động app sau khi deploy |

---

## 🚀 DEPLOY LẦN ĐẦU (deploy.sh)

### Cách dùng:

```bash
# Download script
curl -O https://raw.githubusercontent.com/Clarence161095/news-vn-en-jp/develop/deploy.sh
chmod +x deploy.sh

# Chạy
./deploy.sh
```

### Script sẽ làm gì:

1. ✅ Clone repository từ GitHub
2. ✅ Tạo virtual environment (venv)
3. ✅ Activate venv
4. ✅ Install tất cả dependencies
5. ✅ Hiển thị hướng dẫn start app

### Output mẫu:

```
🚀 Starting deployment of News App...
======================================
📥 Step 1: Cloning repository...
✅ Repository cloned successfully
📦 Step 2: Creating virtual environment...
✅ Virtual environment created
🔄 Step 3: Activating virtual environment...
✅ Virtual environment activated
📚 Step 4: Installing dependencies...
✅ Dependencies installed successfully

🎉 Deployment completed successfully!
======================================

To start the app, run:
cd news-vn-en-jp
source venv/bin/activate
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

---

## 🔄 UPDATE SOURCE CODE (update.sh)

### Cách dùng:

```bash
cd news-vn-en-jp
./update.sh
```

### Script sẽ làm gì:

1. ✅ Stop app (nếu đang chạy với systemd)
2. ✅ Backup database (articles.db)
3. ✅ Pull code mới từ GitHub (branch develop)
4. ✅ Activate virtual environment
5. ✅ Update dependencies
6. ✅ Restart service (hoặc hiển thị hướng dẫn start)

### Output mẫu:

```
🔄 Updating News App...
======================================
🛑 Step 1: Stopping app (if running as service)...
✅ Service stopped
💾 Step 2: Backing up database...
✅ Database backed up to backups/articles_backup_20251122_210000.db
📥 Step 3: Pulling latest code...
✅ Code updated successfully
🔄 Step 4: Activating virtual environment...
✅ Virtual environment activated
📚 Step 5: Updating dependencies...
✅ Dependencies updated

🎉 Update completed successfully!
======================================
✅ Service restarted
```

### Backup database:

Database được tự động backup vào thư mục `backups/` với timestamp:

```
backups/
├── articles_backup_20251122_210000.db
├── articles_backup_20251122_150000.db
└── articles_backup_20251121_120000.db
```

---

## ▶️ START APP (start.sh)

### Cách dùng:

```bash
cd news-vn-en-jp
./start.sh
```

### Script sẽ làm gì:

1. ✅ Check nếu đang ở đúng thư mục
2. ✅ Activate virtual environment
3. ✅ Start Gunicorn server (4 workers)

### Output mẫu:

```
🚀 Starting News App...
======================================
🔄 Activating virtual environment...
✅ Virtual environment activated
🚀 Starting Gunicorn server...

Server will start at: http://0.0.0.0:5000
Press Ctrl+C to stop

[2025-11-22 21:00:00] [INFO] Starting gunicorn 21.2.0
[2025-11-22 21:00:00] [INFO] Listening at: http://0.0.0.0:5000
[2025-11-22 21:00:00] [INFO] Using worker: sync
[2025-11-22 21:00:00] [INFO] Booting worker with pid: 12345
...
```

---

## 📋 Workflow đầy đủ

### 1️⃣ Lần đầu deploy (trên server mới)

```bash
# Bước 1: Download và chạy deploy script
curl -O https://raw.githubusercontent.com/Clarence161095/news-vn-en-jp/develop/deploy.sh
chmod +x deploy.sh
./deploy.sh

# Bước 2: Vào thư mục và start app
cd news-vn-en-jp
./start.sh

# Hoặc chạy background:
source venv/bin/activate
nohup gunicorn --workers 4 --bind 0.0.0.0:5000 app:app > app.log 2>&1 &
```

### 2️⃣ Khi có code mới (update)

```bash
# Đơn giản chỉ cần:
cd news-vn-en-jp
./update.sh

# Script sẽ tự động backup, pull code, update, và restart
```

### 3️⃣ Restart app

```bash
# Nếu chạy với systemd:
sudo systemctl restart newsapp

# Nếu chạy background với nohup:
pkill gunicorn
./start.sh

# Hoặc:
source venv/bin/activate
nohup gunicorn --workers 4 --bind 0.0.0.0:5000 app:app > app.log 2>&1 &
```

---

## 🔧 Customization

### Thay đổi số workers:

Sửa trong script `start.sh` hoặc chạy thủ công:

```bash
# 2 workers (server nhỏ)
gunicorn --workers 2 --bind 0.0.0.0:5000 app:app

# 8 workers (server mạnh)
gunicorn --workers 8 --bind 0.0.0.0:5000 app:app

# Auto detect (2 x CPU cores + 1)
gunicorn --workers $(( 2 * $(nproc) + 1 )) --bind 0.0.0.0:5000 app:app
```

### Thay đổi port:

```bash
# Port 8000 thay vì 5000
gunicorn --workers 4 --bind 0.0.0.0:8000 app:app
```

### Thay đổi branch:

Sửa trong `update.sh`:

```bash
# Line 47: Thay 'develop' thành 'main' hoặc branch khác
git pull origin main
```

---

## 🛠️ Troubleshooting

### Script báo lỗi "Permission denied"

```bash
chmod +x deploy.sh update.sh start.sh
```

### Script không tìm thấy python3

```bash
# Install Python
sudo apt install python3 python3-pip python3-venv -y
```

### Git pull failed

```bash
# Có thể có local changes conflict
cd news-vn-en-jp
git status
git stash  # Lưu changes tạm thời
./update.sh
git stash pop  # Restore changes
```

### Port 5000 bị chiếm

```bash
# Tìm process
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>
```

---

## 📊 Monitoring

### Xem logs

```bash
# Logs từ nohup
tail -f app.log

# Logs từ systemd
sudo journalctl -u newsapp -f

# Logs chi tiết Gunicorn
tail -f access.log error.log
```

### Check app đang chạy

```bash
# Check process
ps aux | grep gunicorn

# Check port
sudo netstat -tulpn | grep :5000

# Test app
curl http://localhost:5000
```

---

## ⚡ Quick Reference

```bash
# Deploy lần đầu
./deploy.sh && cd news-vn-en-jp && ./start.sh

# Update code
cd news-vn-en-jp && ./update.sh

# Start app
cd news-vn-en-jp && ./start.sh

# Stop app
pkill gunicorn

# View logs
tail -f app.log

# Backup database
cp articles.db backups/articles_backup_$(date +%Y%m%d_%H%M%S).db

# Restore database
cp backups/articles_backup_YYYYMMDD_HHMMSS.db articles.db
```

---

**Scripts make deployment easy! 🚀**
