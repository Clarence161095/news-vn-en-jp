# 🎯 TÓM TẮT: Chạy app trên EC2 với port 5000

## ✅ Giải pháp cho vấn đề của bạn

### Vấn đề:
- ❌ App không truy cập được từ bên ngoài EC2
- ❌ Đã mở Security Group port 5000 nhưng vẫn không hoạt động

### Nguyên nhân:
- Gunicorn phải bind `0.0.0.0:5000` (không phải `127.0.0.1:5000`)
- App phải chạy background để không bị stop khi logout SSH

### Giải pháp:
✅ Sử dụng script `start-background.sh` đã tạo sẵn

---

## 🚀 CÁCH DEPLOY ĐÚNG (3 bước)

### Bước 1: Clone và cài đặt

```bash
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Bước 2: Start app chạy ngầm

```bash
./start-background.sh
```

**Script này sẽ:**
- ✅ Bind đúng địa chỉ: `0.0.0.0:5000` 
- ✅ Chạy background (daemon mode)
- ✅ Tạo logs vào thư mục `logs/`
- ✅ Hiển thị Public IP để truy cập

### Bước 3: Kiểm tra

```bash
./status.sh
```

**Output mẫu:**
```
📊 News App Status
======================================
✅ Status: RUNNING

Access URLs:
  Local:    http://localhost:5000
  Private:  http://172.31.45.123:5000
  Public:   http://54.123.45.67:5000  👈 DÙNG URL NÀY
```

---

## 🔧 Security Group (AWS Console)

### Inbound Rules phải có:

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| SSH | TCP | 22 | My IP | SSH access |
| **Custom TCP** | **TCP** | **5000** | **0.0.0.0/0** | **Flask App** ← QUAN TRỌNG |

**Cách kiểm tra:**
1. Vào AWS Console → EC2 → Security Groups
2. Chọn Security Group của instance
3. Tab "Inbound rules"
4. Đảm bảo có rule: Type = Custom TCP, Port = 5000, Source = 0.0.0.0/0

---

## 📋 Scripts đã tạo

| Script | Chức năng | Khi nào dùng |
|--------|-----------|--------------|
| `start-background.sh` | Start app chạy ngầm | **Dùng cho production** ⭐ |
| `stop.sh` | Stop app | Khi cần dừng app |
| `status.sh` | Check status + Public IP | Check xem app đang chạy không |
| `start.sh` | Start foreground | Dùng để test/debug |
| `update.sh` | Update code từ GitHub | Khi có code mới |

---

## ✅ Checklist để app hoạt động

### 1. App đang chạy đúng cách:

```bash
cd news-vn-en-jp
./status.sh
```

Phải thấy:
- ✅ `Status: RUNNING`
- ✅ `0.0.0.0:5000` (không phải 127.0.0.1)
- ✅ Public IP hiển thị

### 2. Security Group đúng:

AWS Console → EC2 → Security Groups:
- ✅ Port 5000, TCP, Source: 0.0.0.0/0

### 3. Test từ local:

```bash
# Từ EC2 server
curl http://localhost:5000

# Từ máy tính của bạn (thay PUBLIC_IP)
curl http://54.123.45.67:5000
```

### 4. Browser:

```
http://YOUR_EC2_PUBLIC_IP:5000
```

Phải thấy trang chủ của app.

---

## 🐛 Troubleshooting nhanh

### ❌ Vẫn không truy cập được?

**Check 1: App đang chạy?**
```bash
./status.sh
```

**Check 2: Bind đúng địa chỉ?**
```bash
sudo netstat -tulpn | grep :5000
# Phải thấy: 0.0.0.0:5000 (không phải 127.0.0.1:5000)
```

**Check 3: Security Group?**
- Vào AWS Console
- EC2 → Instance → Security tab
- Click vào Security Group
- Inbound rules → Phải có port 5000

**Check 4: Test local?**
```bash
curl http://localhost:5000
# Nếu OK → Vấn đề ở Security Group
# Nếu fail → Vấn đề ở app
```

### ❌ App bị stop sau khi logout SSH?

**Giải pháp:**
```bash
./stop.sh
./start-background.sh  # Phải dùng script này!
```

Không dùng:
- ❌ `python app.py` (chạy dev server)
- ❌ `gunicorn app:app` (không có background)
- ❌ `nohup ... &` thủ công (có thể sai config)

### ❌ Port 5000 bị chiếm?

```bash
sudo lsof -i :5000
sudo kill -9 <PID>
./start-background.sh
```

---

## 📊 View Logs

```bash
# Real-time logs
tail -f logs/error.log   # Error logs
tail -f logs/access.log  # Access logs

# Last 50 lines
tail -50 logs/error.log

# All logs
tail -f logs/*.log
```

---

## 🔄 Update code (khi push code mới lên GitHub)

```bash
cd news-vn-en-jp
./update.sh
```

Script sẽ tự động:
1. Stop app
2. Backup database
3. Pull code mới
4. Update dependencies
5. Restart app

---

## 💡 Tips

### 1. Lấy Public IP nhanh

```bash
./status.sh | grep Public
```

### 2. Monitor real-time

```bash
# Terminal 1: Logs
tail -f logs/*.log

# Terminal 2: Status
watch -n 5 './status.sh'
```

### 3. Restart nhanh

```bash
./stop.sh && ./start-background.sh
```

### 4. One-liner deploy

```bash
git clone https://github.com/Clarence161095/news-vn-en-jp.git && \
cd news-vn-en-jp && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
./start-background.sh
```

---

## 📞 Quick Commands Reference

```bash
# Deploy
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Start (background)
./start-background.sh

# Check status
./status.sh

# Stop
./stop.sh

# Update
./update.sh

# Logs
tail -f logs/error.log
tail -f logs/access.log

# Restart
./stop.sh && ./start-background.sh
```

---

## 🎉 Kết luận

**Để app chạy đúng trên EC2 port 5000:**

1. ✅ Dùng `./start-background.sh` (không phải python app.py)
2. ✅ Security Group mở port 5000 cho 0.0.0.0/0
3. ✅ Kiểm tra với `./status.sh`
4. ✅ Truy cập: `http://PUBLIC_IP:5000`

**Nếu vẫn không được, check:**
- `./status.sh` → App có đang chạy?
- `sudo netstat -tulpn | grep :5000` → Bind đúng 0.0.0.0?
- AWS Console → Security Group → Port 5000 đã mở?
- `tail -f logs/error.log` → Có lỗi gì không?

---

**Total deployment time: ~5 phút! 🚀**
