# 🆘 KHẮC PHỤC LỖI SQLITE TRÊN EC2

## ❌ Vấn đề

- SQLite database bị lỗi/corrupt trên EC2
- App không khởi động được
- Database connection errors

## ✅ Giải pháp: Dùng script `reset.sh`

### 🚀 Cách sử dụng (1 lệnh)

```bash
cd news-vn-en-jp
./reset.sh
```

Nhấn `y` khi được hỏi.

### Script sẽ làm gì?

1. ✅ **Stop app** đang chạy
2. ✅ **Backup database** hiện tại → `backups/articles_reset_backup_*.db`
3. ✅ **Xóa database** cũ (bị lỗi)
4. ✅ **Xóa virtual environment** cũ
5. ✅ **Tạo lại venv** mới
6. ✅ **Install dependencies** từ `requirements.txt`
7. ✅ **Tạo database** mới (sạch)
8. ✅ **Start app** chạy ngầm trên port 5000

### Output thành công

```
🎉 Reset Complete!
======================================
✅ App is running and responding!
🌐 Access your app at: http://54.123.45.67:5000
```

---

## 📋 Checklist sau khi reset

### 1. Check status

```bash
./status.sh
```

Phải thấy:
- ✅ Status: RUNNING
- ✅ Port 5000: LISTENING  
- ✅ Public IP hiển thị

### 2. Test HTTP

```bash
curl http://localhost:5000
```

Phải trả về HTML (không phải error).

### 3. Test browser

Mở browser:
```
http://YOUR_EC2_PUBLIC_IP:5000
```

Phải hiển thị trang chủ.

---

## 🔍 Nếu vẫn lỗi

### Check logs

```bash
tail -50 logs/error.log
```

### Check database

```bash
ls -lh articles.db
sqlite3 articles.db "SELECT count(*) FROM sqlite_master WHERE type='table';"
```

Phải có 2 tables.

### Check port

```bash
sudo netstat -tulpn | grep :5000
```

Phải thấy `0.0.0.0:5000`.

---

## 💾 Restore database backup

Nếu cần restore database cũ:

```bash
# List backups
ls -lh backups/

# Stop app
./stop.sh

# Restore
cp backups/articles_reset_backup_YYYYMMDD_HHMMSS.db articles.db

# Start app
./start-background.sh
```

---

## ⚡ Quick Commands

```bash
# Reset toàn bộ
./reset.sh

# Reset không cần confirm
yes | ./reset.sh

# Reset + check status
./reset.sh && sleep 5 && ./status.sh

# Backup manual trước khi reset
cp articles.db backup_$(date +%Y%m%d).db && ./reset.sh
```

---

## 📊 So sánh các scripts

| Khi gặp vấn đề | Dùng script nào |
|----------------|-----------------|
| Code mới từ GitHub | `./update.sh` |
| Cần restart app | `./stop.sh && ./start-background.sh` |
| **Database lỗi** | **`./reset.sh`** ⭐ |
| **Dependencies lỗi** | **`./reset.sh`** ⭐ |
| **App không start** | **`./reset.sh`** ⭐ |

---

## ⚠️ Lưu ý quan trọng

- ❌ Database sẽ bị xóa (có backup tự động)
- ❌ Tất cả dữ liệu trong app sẽ mất
- ✅ Nhưng app sẽ chạy sạch, không lỗi
- ✅ Có thể restore từ backup

---

**Script `reset.sh` là "panic button" để fix mọi vấn đề! 🔄**
