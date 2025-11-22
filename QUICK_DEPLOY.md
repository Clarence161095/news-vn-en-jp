# ⚡ Quick Deploy Guide

## 🚀 Deployment lần đầu (First Time)

### Cách 1: Sử dụng script tự động

```bash
# Download và chạy script deploy
curl -O https://raw.githubusercontent.com/Clarence161095/news-vn-en-jp/develop/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### Cách 2: Deploy thủ công

```bash
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

---

## 🔄 Update source code (Khi có thay đổi)

### Cách 1: Sử dụng script tự động

```bash
cd news-vn-en-jp
./update.sh
```

Script sẽ tự động:
- ✅ Stop service (nếu đang chạy)
- ✅ Backup database
- ✅ Pull code mới từ GitHub
- ✅ Update dependencies
- ✅ Restart service

### Cách 2: Update thủ công

```bash
cd news-vn-en-jp

# Stop app nếu đang chạy
# Nếu chạy với systemd:
sudo systemctl stop newsapp

# Nếu chạy background:
pkill gunicorn

# Pull code mới
git pull origin develop

# Activate venv và update
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
# Hoặc:
sudo systemctl start newsapp
```

---

## 🎯 Start/Stop App

### Start app (Foreground - recommended cho testing)

```bash
cd news-vn-en-jp
./start.sh
```

Press `Ctrl+C` to stop.

### Start app (Background - recommended cho production)

```bash
cd news-vn-en-jp
./start-background.sh
```

Script sẽ:
- ✅ Start Gunicorn với 4 workers
- ✅ Bind to `0.0.0.0:5000` (accessible from outside)
- ✅ Save logs to `logs/access.log` and `logs/error.log`
- ✅ Run as daemon (background process)
- ✅ Show public IP để truy cập

### Check status

```bash
cd news-vn-en-jp
./status.sh
```

Sẽ hiển thị:
- ✅ App đang chạy hay không
- ✅ Process ID (PID)
- ✅ Port status
- ✅ Access URLs (local, private IP, public IP)
- ✅ Recent logs

### Stop app

```bash
cd news-vn-en-jp
./stop.sh
```

Hoặc thủ công:

```bash
# Stop gracefully
pkill -f 'gunicorn.*app:app'

# Force stop
pkill -9 -f 'gunicorn.*app:app'

# Nếu chạy với systemd:
sudo systemctl stop newsapp
```

---

## 📊 Monitoring

### Xem logs

```bash
# Nếu chạy background:
tail -f app.log

# Nếu chạy với systemd:
sudo journalctl -u newsapp -f
```

### Check status

```bash
# Nếu chạy với systemd:
sudo systemctl status newsapp

# Hoặc check process:
ps aux | grep gunicorn
```

---

## 🔧 Troubleshooting

### Port 5000 đã được sử dụng

```bash
# Tìm process đang dùng port 5000
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>
```

### Virtual environment lỗi

```bash
# Xóa và tạo lại
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database bị lỗi

```bash
# Restore từ backup
cp backups/articles_backup_YYYYMMDD_HHMMSS.db articles.db

# Hoặc tạo mới (MẤT DỮ LIỆU!)
rm articles.db
python app.py  # Database sẽ tự động tạo
```

---

## 📦 Scripts có sẵn

| Script | Mô tả |
|--------|-------|
| `deploy.sh` | Deploy lần đầu tiên |
| `update.sh` | Update source code + dependencies |
| `start.sh` | Start app ở foreground |

### Cách sử dụng scripts

```bash
# Make executable (chỉ cần làm 1 lần)
chmod +x deploy.sh update.sh start.sh

# Run
./deploy.sh   # First time deploy
./update.sh   # Update code
./start.sh    # Start app
```

---

## ⚡ One-liner Commands

### Quick start (đã deploy)

```bash
cd news-vn-en-jp && source venv/bin/activate && gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### Quick update

```bash
cd news-vn-en-jp && git pull && source venv/bin/activate && pip install -r requirements.txt --upgrade && sudo systemctl restart newsapp
```

### Quick backup

```bash
cd news-vn-en-jp && cp articles.db backups/articles_backup_$(date +%Y%m%d_%H%M%S).db
```

---

## 🎓 Tips

1. **Luôn backup database trước khi update**:
   ```bash
   cp articles.db articles_backup.db
   ```

2. **Test trước trên development**:
   ```bash
   git checkout develop
   python app.py  # Test với Flask dev server
   ```

3. **Xem thay đổi trước khi pull**:
   ```bash
   git fetch origin
   git log HEAD..origin/develop --oneline
   ```

4. **Rollback nếu có lỗi**:
   ```bash
   git log --oneline -5  # Xem commit history
   git reset --hard <commit-hash>  # Quay về commit trước
   ```

---

**Happy deploying! 🚀**
