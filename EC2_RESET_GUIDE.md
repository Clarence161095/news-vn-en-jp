# 🔄 EC2 Reset Guide - Quick Fix for Database/Dependency Issues

## 📋 Khi nào dùng script này?

Sử dụng `reset-linux.sh` khi gặp các vấn đề sau trên EC2:

- ❌ SQLite database errors
- ❌ Dependency conflicts
- ❌ App crashes or won't start
- ❌ Cache corruption
- ❌ After major code changes
- ❌ When you need a fresh start

## 🚀 Cách sử dụng trên EC2

### Bước 1: SSH vào EC2

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

### Bước 2: Di chuyển vào thư mục project

```bash
cd news-vn-en-jp
```

### Bước 3: Chạy reset script

```bash
bash reset-linux.sh
```

Hoặc:

```bash
chmod +x reset-linux.sh
./reset-linux.sh
```

### Bước 4: Xác nhận

Script sẽ hỏi xác nhận:
```
Continue? (y/N): y
```

Nhấn `y` và Enter để tiếp tục.

## 📊 Script sẽ làm gì?

### ✅ 8 bước tự động:

1. **Stop app** - Dừng Gunicorn đang chạy
2. **Backup database** - Sao lưu DB vào `backups/`
3. **Clean files** - Xóa DB cũ, cache, logs
4. **Check Python** - Phát hiện Python 3
5. **Setup venv** - Tạo môi trường ảo mới
6. **Install deps** - Cài đặt lại tất cả dependencies
7. **Init database** - Tạo DB mới với schema đúng
8. **Start app** - Khởi động Gunicorn trên 0.0.0.0:5000

### 📦 Backup tự động

Tất cả backup được lưu trong `backups/`:
```
backups/
├── articles_reset_backup_20241122_230312.db
├── katakana_cache_backup_20241122_230312.json
└── ...
```

## ⏱️ Thời gian chạy

- **Tổng thời gian**: ~2-3 phút
- **Download packages**: ~1-2 phút
- **Database init**: ~5 giây
- **App startup**: ~3 giây

## ✅ Kiểm tra sau khi reset

Script tự động kiểm tra:

```
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

🎉 Reset Complete!
✅ App is running and ready!
```

## 🔍 Troubleshooting

### Nếu script fail:

#### 1. Python not found
```bash
# Amazon Linux 2
sudo yum install python3 -y

# Ubuntu/Debian
sudo apt install python3 python3-venv -y
```

#### 2. App không start
```bash
# Xem error log
tail -f logs/error.log

# Kiểm tra port
sudo netstat -tuln | grep 5000

# Kiểm tra process
ps aux | grep gunicorn
```

#### 3. Permission denied
```bash
chmod +x reset-linux.sh
```

#### 4. Port 5000 đã được dùng
```bash
# Tìm process
sudo lsof -i :5000

# Hoặc
sudo netstat -tulnp | grep :5000

# Kill process
sudo kill -9 <PID>
```

### Nếu HTTP test FAILED:

```bash
# Đợi 10 giây cho app khởi động
sleep 10
curl http://localhost:5000

# Kiểm tra Security Group
# - Inbound rule: TCP port 5000 from 0.0.0.0/0
```

## 📝 Logs

Sau khi reset, kiểm tra logs:

```bash
# Xem real-time error log
tail -f logs/error.log

# Xem real-time access log
tail -f logs/access.log

# Xem 50 dòng cuối error log
tail -50 logs/error.log
```

## 🛠️ Commands hữu ích sau reset

```bash
# Kiểm tra status
./status.sh

# Dừng app
./stop.sh

# Khởi động lại
./start-background.sh

# Xem tất cả backups
ls -lh backups/

# Restore từ backup (nếu cần)
cp backups/articles_reset_backup_YYYYMMDD_HHMMSS.db articles.db
```

## ⚠️ Lưu ý quan trọng

### 1. Database sẽ trống sau reset
- Tất cả articles sẽ bị xóa
- Nhưng đã có backup trong `backups/`
- Để restore: `cp backups/latest.db articles.db`

### 2. App bind 0.0.0.0:5000
- Cho phép truy cập từ bên ngoài
- **Bắt buộc** cho EC2
- Security Group phải mở port 5000

### 3. Gunicorn settings
- Workers: 4
- Threads per worker: 2
- Mode: daemon (background)
- Logs: `logs/access.log`, `logs/error.log`

## 🔄 So sánh với các scripts khác

| Script | Mục đích | Khi nào dùng |
|--------|----------|--------------|
| `deploy.sh` | First-time deployment | Lần đầu setup EC2 |
| `update.sh` | Update code from GitHub | Có code mới |
| `start-background.sh` | Start app | App đã dừng |
| `stop.sh` | Stop app | Cần dừng app |
| **`reset-linux.sh`** | **Full reset** | **App lỗi/DB corrupt** |

## 🎯 Use Cases

### Use Case 1: SQLite Errors
```bash
cd ~/news-vn-en-jp
bash reset-linux.sh  # Tạo DB mới, fix lỗi
```

### Use Case 2: Dependency Conflicts
```bash
bash reset-linux.sh  # Reinstall tất cả packages
```

### Use Case 3: Sau khi update code lớn
```bash
git pull origin main  # Pull code mới
bash reset-linux.sh   # Reset environment
```

### Use Case 4: App không start được
```bash
bash reset-linux.sh   # Clean start
```

## ✨ Features

- ✅ **One-command reset** - Chỉ 1 lệnh
- ✅ **Automatic backup** - Tự động backup DB
- ✅ **Safe cleanup** - Xóa sạch nhưng an toàn
- ✅ **Fresh install** - Dependencies mới 100%
- ✅ **Auto verification** - Tự động kiểm tra
- ✅ **Detailed status** - Report chi tiết
- ✅ **Error handling** - Xử lý lỗi tốt
- ✅ **Production ready** - Dùng Gunicorn, bind 0.0.0.0

## 📞 Support

Nếu gặp vấn đề:

1. Check logs: `tail -f logs/error.log`
2. Check status: `./status.sh`
3. Check process: `ps aux | grep gunicorn`
4. Check port: `sudo netstat -tuln | grep 5000`

---

**Last updated**: November 22, 2024
**Script version**: 1.0
**Tested on**: Amazon Linux 2, Ubuntu 20.04/22.04
