# 🚀 Hướng dẫn Deploy lên AWS EC2

## Bước 1: Chuẩn bị EC2 Instance

### 1.1. Tạo EC2 Instance

1. Đăng nhập vào AWS Console
2. Chọn **EC2** → **Launch Instance**
3. Cấu hình:
   - **Name**: `news-vn-en-jp-server`
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: `t2.micro` (free tier) hoặc `t3.small`
   - **Key Pair**: Tạo hoặc chọn key pair có sẵn (để SSH)
   - **Security Group**:
     - SSH (22) - Cho phép từ IP của bạn
     - HTTP (80) - Cho phép từ mọi nơi (0.0.0.0/0)
     - HTTPS (443) - Cho phép từ mọi nơi (0.0.0.0/0)
   - **Storage**: 8GB trở lên

4. Launch instance

### 1.2. Kết nối SSH

```bash
# Thay your-key.pem và ec2-public-ip bằng giá trị thực tế
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@ec2-public-ip
```

## Bước 2: Cài đặt môi trường trên EC2

### 2.1. Cập nhật hệ thống

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2. Cài đặt Python và dependencies

```bash
# Cài Python 3 và pip
sudo apt install python3 python3-pip python3-venv -y

# Cài Git
sudo apt install git -y

# Cài Nginx
sudo apt install nginx -y
```

## Bước 3: Deploy ứng dụng

### 3.1. Clone repository

```bash
cd ~
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp
```

### 3.2. Tạo virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3. Cài đặt dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.4. Test chạy app

```bash
# Chạy thử để kiểm tra
python app.py

# Nếu chạy OK, nhấn Ctrl+C để dừng
```

## Bước 4: Cấu hình Gunicorn

### 4.1. Test Gunicorn

```bash
# Chạy với Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Test từ trình duyệt: http://ec2-public-ip:5000
# Nếu OK, nhấn Ctrl+C
```

### 4.2. Tạo systemd service

Tạo file service:

```bash
sudo nano /etc/systemd/system/newsapp.service
```

Nội dung file:

```ini
[Unit]
Description=News App Gunicorn Service
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/news-vn-en-jp
Environment="PATH=/home/ubuntu/news-vn-en-jp/venv/bin"
ExecStart=/home/ubuntu/news-vn-en-jp/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/home/ubuntu/news-vn-en-jp/newsapp.sock \
    --access-logfile /home/ubuntu/news-vn-en-jp/access.log \
    --error-logfile /home/ubuntu/news-vn-en-jp/error.log \
    app:app

[Install]
WantedBy=multi-user.target
```

Lưu file (Ctrl+X, Y, Enter)

### 4.3. Khởi động service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Khởi động service
sudo systemctl start newsapp

# Enable service (tự động chạy khi boot)
sudo systemctl enable newsapp

# Kiểm tra status
sudo systemctl status newsapp
```

## Bước 5: Cấu hình Nginx

### 5.1. Tạo Nginx config

```bash
sudo nano /etc/nginx/sites-available/newsapp
```

Nội dung:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Thay bằng domain hoặc IP của bạn

    # Logs
    access_log /var/log/nginx/newsapp_access.log;
    error_log /var/log/nginx/newsapp_error.log;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/news-vn-en-jp/newsapp.sock;
        
        # Timeout settings
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }

    # Static files (nếu có)
    location /static {
        alias /home/ubuntu/news-vn-en-jp/static;
        expires 30d;
    }

    # Client max body size (cho upload JSON)
    client_max_body_size 10M;
}
```

### 5.2. Enable site

```bash
# Tạo symbolic link
sudo ln -s /etc/nginx/sites-available/newsapp /etc/nginx/sites-enabled/

# Test cấu hình
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 5.3. Test

Truy cập: `http://your-ec2-public-ip` hoặc `http://your-domain.com`

## Bước 6: Cài đặt SSL (HTTPS) với Let's Encrypt

### 6.1. Cài Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 6.2. Lấy SSL certificate

```bash
# Thay your-domain.com bằng domain thực tế
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Làm theo hướng dẫn:

- Nhập email
- Đồng ý Terms of Service
- Chọn redirect HTTP sang HTTPS (khuyến nghị: Yes)

### 6.3. Auto-renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot tự động setup cron job để renew
```

## Bước 7: Bảo mật

### 7.1. Cấu hình Firewall (UFW)

```bash
# Cài UFW
sudo apt install ufw -y

# Cấu hình
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'

# Enable
sudo ufw enable

# Check status
sudo ufw status
```

### 7.2. Update Security Group trên AWS

- SSH (22): Chỉ cho phép IP của bạn
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0

## Bước 8: Quản lý ứng dụng

### 8.1. Xem logs

```bash
# Application logs
tail -f /home/ubuntu/news-vn-en-jp/error.log
tail -f /home/ubuntu/news-vn-en-jp/access.log

# Nginx logs
sudo tail -f /var/log/nginx/newsapp_error.log
sudo tail -f /var/log/nginx/newsapp_access.log

# Service logs
sudo journalctl -u newsapp -f
```

### 8.2. Restart service

```bash
sudo systemctl restart newsapp
sudo systemctl restart nginx
```

### 8.3. Stop service

```bash
sudo systemctl stop newsapp
```

### 8.4. Update code

```bash
cd /home/ubuntu/news-vn-en-jp
git pull origin main  # hoặc develop
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart newsapp
```

## Bước 9: Backup

### 9.1. Backup database

```bash
# Tạo script backup
nano ~/backup.sh
```

Nội dung:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR

# Backup database
cp /home/ubuntu/news-vn-en-jp/articles.db $BACKUP_DIR/articles_$DATE.db

# Xóa backup cũ hơn 7 ngày
find $BACKUP_DIR -name "articles_*.db" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Phân quyền:

```bash
chmod +x ~/backup.sh
```

### 9.2. Cron job cho backup

```bash
crontab -e
```

Thêm dòng (backup hàng ngày lúc 2h sáng):

```cron
0 2 * * * /home/ubuntu/backup.sh >> /home/ubuntu/backup.log 2>&1
```

## Bước 10: Monitoring

### 10.1. Xem resource usage

```bash
# CPU và RAM
htop

# Disk space
df -h

# Process
ps aux | grep gunicorn
```

### 10.2. Test performance

```bash
# Test từ local machine
curl -I http://your-domain.com

# Load test (nếu cài apache2-utils)
sudo apt install apache2-utils -y
ab -n 100 -c 10 http://your-domain.com/
```

## ✅ Checklist sau khi deploy

- [ ] App chạy tại port 80/443
- [ ] Nginx hoạt động bình thường
- [ ] SSL certificate đã cài (HTTPS)
- [ ] Firewall đã cấu hình
- [ ] Service tự động chạy khi reboot
- [ ] Backup được setup
- [ ] Logs được monitor

## 🐛 Troubleshooting

### App không khởi động

```bash
# Check service status
sudo systemctl status newsapp

# Check logs
sudo journalctl -u newsapp -n 50

# Check permissions
ls -la /home/ubuntu/news-vn-en-jp/
```

### Nginx 502 Bad Gateway

```bash
# Check if newsapp.sock exists
ls -la /home/ubuntu/news-vn-en-jp/newsapp.sock

# Check Gunicorn is running
ps aux | grep gunicorn

# Restart service
sudo systemctl restart newsapp
sudo systemctl restart nginx
```

### Database locked

```bash
# Check processes using DB
sudo lsof | grep articles.db

# Restart app
sudo systemctl restart newsapp
```

## 📞 Support

Nếu gặp vấn đề, kiểm tra:

1. Logs: `/var/log/nginx/` và `~/news-vn-en-jp/error.log`
2. Service status: `sudo systemctl status newsapp nginx`
3. Port listening: `sudo netstat -tulpn | grep LISTEN`

---

**Good luck with your deployment! 🚀**
