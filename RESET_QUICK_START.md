# 🔄 Quick Start - EC2 Reset Script

## Trên EC2 (Linux):

```bash
# 1. Pull code mới nhất
cd news-vn-en-jp
git pull origin main

# 2. Chạy reset script
chmod +x reset-linux.sh
./reset-linux.sh

# 3. Nhấn 'y' để xác nhận

# 4. Đợi 2-3 phút, script sẽ tự động:
#    - Stop app
#    - Backup database
#    - Clean files
#    - Reinstall dependencies
#    - Create fresh database
#    - Start app on 0.0.0.0:5000
```

## Kiểm tra sau khi reset:

```bash
# Check status
./status.sh

# Test local
curl http://localhost:5000

# View logs
tail -f logs/error.log
```

## Truy cập app:

```
http://YOUR_EC2_PUBLIC_IP:5000
```

**⚠️ Nhớ mở port 5000 trong Security Group!**

---

📚 **Chi tiết:** Xem `EC2_RESET_GUIDE.md`
