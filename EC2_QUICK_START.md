# 🚀 Quick Start trên EC2

## ⚡ Deploy nhanh (3 bước)

### 1️⃣ Trên EC2: Clone và cài đặt

```bash
# Clone repository
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp

# Tạo venv và install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Start app chạy ngầm (background)

```bash
./start-background.sh
```

✅ App sẽ chạy ở background trên port 5000

### 3️⃣ Kiểm tra status

```bash
./status.sh
```

Output sẽ hiển thị Public IP:

```
📊 News App Status
======================================
✅ Status: RUNNING

Access URLs:
  Local:    http://localhost:5000
  Private:  http://172.31.xx.xx:5000
  Public:   http://xx.xx.xx.xx:5000  ← Dùng URL này

To view logs:
  tail -f logs/error.log
  tail -f logs/access.log
```

---

## 🔧 Security Group Settings

### Cấu hình Inbound Rules:

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| SSH | TCP | 22 | My IP | SSH access |
| Custom TCP | TCP | 5000 | 0.0.0.0/0 | Flask app |
| HTTP | TCP | 80 | 0.0.0.0/0 | Nginx (optional) |
| HTTPS | TCP | 443 | 0.0.0.0/0 | SSL (optional) |

**Lưu ý:** Nếu chỉ test, chỉ cần mở port 5000 là đủ.

---

## 🎯 Commands cần nhớ

### Start/Stop/Status

```bash
./start-background.sh   # Start app (chạy ngầm)
./stop.sh               # Stop app
./status.sh             # Check status + lấy Public IP
```

### View Logs

```bash
tail -f logs/access.log  # Access logs
tail -f logs/error.log   # Error logs
tail -f logs/*.log       # All logs
```

### Update Code

```bash
./update.sh              # Auto: backup DB, pull code, restart
```

---

## ✅ Checklist sau khi deploy

- [ ] App chạy: `./status.sh` hiển thị "RUNNING"
- [ ] Security Group: Port 5000 đã mở cho 0.0.0.0/0
- [ ] Truy cập được: `curl http://PUBLIC_IP:5000`
- [ ] Logs OK: `tail -f logs/error.log` không có lỗi

---

## 🐛 Troubleshooting

### 1. Không truy cập được từ browser

**Nguyên nhân:** Security Group chưa mở port 5000

**Fix:**

```bash
# Kiểm tra app đang chạy
./status.sh

# Kiểm tra port
sudo netstat -tulpn | grep :5000

# Nếu thấy "0.0.0.0:5000" → OK
# Nếu thấy "127.0.0.1:5000" → Sai! Phải bind 0.0.0.0
```

**Giải pháp:** Đảm bảo Gunicorn bind `0.0.0.0:5000` (script đã config sẵn)

### 2. App bị stop sau khi logout SSH

**Nguyên nhân:** Chưa chạy background

**Fix:**

```bash
# Stop app hiện tại (nếu có)
./stop.sh

# Start lại ở background
./start-background.sh

# Kiểm tra
./status.sh

# Logout SSH và test lại
exit
# SSH lại và check
./status.sh
```

### 3. Port 5000 bị chiếm

```bash
# Tìm process đang dùng port
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>

# Hoặc dùng script
./stop.sh
./start-background.sh
```

### 4. Permission denied khi chạy script

```bash
chmod +x *.sh
```

---

## 📊 Performance Tips

### 1. Tăng số workers (server mạnh)

Sửa file `start-background.sh`:

```bash
# Line 38: Thay --workers 4 thành 8
--workers 8 \
```

### 2. Giảm số workers (server yếu - t2.micro)

```bash
# Sửa thành 2 workers
--workers 2 \
```

### 3. Auto restart khi server reboot

Tạo systemd service (xem DEPLOY.md chi tiết):

```bash
sudo nano /etc/systemd/system/newsapp.service
# Copy config từ DEPLOY.md
sudo systemctl enable newsapp
```

---

## 🔄 Workflow hàng ngày

### Sáng: Check status

```bash
ssh -i your-key.pem ubuntu@ec2-public-ip
cd news-vn-en-jp
./status.sh
tail -f logs/access.log  # Xem traffic
```

### Khi có code mới: Update

```bash
cd news-vn-en-jp
./update.sh  # Tự động: backup, pull, restart
```

### Tối: Backup database

```bash
cd news-vn-en-jp
cp articles.db backups/articles_$(date +%Y%m%d).db
```

---

## 🌐 Access URLs

Sau khi deploy, bạn có thể truy cập qua:

1. **Public IP** (recommended):
   ```
   http://YOUR_EC2_PUBLIC_IP:5000
   ```

2. **Public DNS**:
   ```
   http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com:5000
   ```

3. **Domain** (nếu đã setup):
   ```
   http://yourdomain.com:5000
   ```

**Để bỏ port :5000**, cần setup Nginx reverse proxy (xem DEPLOY.md)

---

## ✨ Next Steps

### 1. Setup Nginx (để bỏ :5000 từ URL)

```bash
sudo apt install nginx -y
# Follow DEPLOY.md section 5
```

### 2. Setup SSL (HTTPS)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

### 3. Setup Monitoring

```bash
# Install htop
sudo apt install htop -y

# Monitor resources
htop

# Monitor logs real-time
tail -f logs/*.log
```

---

## 📞 Quick Support

**App không chạy?**

```bash
./status.sh              # Check status
tail -f logs/error.log   # Check errors
./stop.sh && ./start-background.sh  # Restart
```

**Cần help?**

1. Check logs: `tail -f logs/error.log`
2. Check status: `./status.sh`
3. Check security group: Port 5000 opened?
4. Test local: `curl http://localhost:5000`

---

**Deployment time: ~5 minutes! 🎉**
