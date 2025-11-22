# ��� News Vietnamese-English Reader

Ứng dụng đọc báo song ngữ Việt-Anh với tự động phiên âm IPA cho tiếng Anh.

## ✨ Tính năng

- **Song ngữ Việt-Anh**: Đọc bài viết bằng tiếng Việt, tiếng Anh, hoặc cả hai
- **Tự động IPA**: Phát âm IPA tự động cho tiếng Anh (dùng thư viện eng-to-ipa)
- **Cache thông minh**: IPA được cache trong database để tăng tốc độ
- **Import JSON**: Nhập bài viết qua JSON với validation
- **Responsive UI**: Giao diện đơn giản, dễ sử dụng

## ��� Cài đặt nhanh

### 1. Reset và khởi động (Windows)

```bash
sh reset.sh
```

Script này sẽ:
- Dừng app đang chạy
- Backup database cũ
- Xóa và tạo lại database
- Cài đặt dependencies
- Khởi động app trên port 5000

### 2. Truy cập ứng dụng

- **Trang chủ**: http://localhost:5000
- **Import bài viết**: http://localhost:5000/import

## ��� Định dạng JSON import

```json
{
  "title_vi": "Tiêu đề tiếng Việt",
  "title_en": "English Title",
  "content_vi": "<p>Nội dung tiếng Việt</p>",
  "content_en": "<p>English content</p>",
  "category": "technology"
}
```

**Lưu ý**:
- Phải có ít nhất 1 title (title_vi hoặc title_en)
- Phải có ít nhất 1 content (content_vi hoặc content_en)
- Hỗ trợ import đơn object hoặc array of objects
- Validation tự động kiểm tra cấu trúc JSON

## ���️ Scripts hữu ích

### Windows
```bash
sh reset.sh      # Reset và khởi động lại
sh status.sh     # Kiểm tra trạng thái
sh stop.sh       # Dừng app
```

### Linux/macOS
```bash
./reset-linux.sh    # Reset và khởi động lại
./status.sh         # Kiểm tra trạng thái
./stop.sh           # Dừng app
```

## ���️ Cấu trúc Database

### Table: articles
- `id`: Primary key
- `title_vi`: Tiêu đề tiếng Việt
- `title_en`: Tiêu đề tiếng Anh
- `content_vi`: Nội dung tiếng Việt
- `content_en`: Nội dung tiếng Anh
- `category`: Danh mục
- `created_at`: Ngày tạo
- `updated_at`: Ngày cập nhật

### Table: article_cache
- `article_id`: Foreign key → articles.id
- `title_en_ipa`: Tiêu đề tiếng Anh có IPA
- `content_en_ipa`: Nội dung tiếng Anh có IPA
- `cached_at`: Ngày cache

## ⚡ Tối ưu hóa hiệu năng

1. **IPA Caching**: Kết quả IPA được lưu trong database, chỉ tính 1 lần
2. **Lazy Loading**: IPA chỉ được tạo khi xem bài viết lần đầu
3. **In-memory Cache**: Cache IPA lookups trong runtime để tránh trùng lặp
4. **Optimized Regex**: Dùng compiled regex patterns

## ��� Cấu hình

### Requirements
- Python 3.7+
- Flask 3.0.0
- eng-to-ipa 0.0.2
- gunicorn 21.2.0

### Cài đặt thủ công

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi động
python app.py
```

## ��� Logs

```bash
# Xem access logs
tail -f logs/access.log

# Xem error logs
tail -f logs/error.log
```

## ��� Xử lý lỗi thường gặp

### Port 5000 đã được sử dụng
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:5000 | xargs kill -9
```

### Import JSON lỗi
- Kiểm tra cú pháp JSON (dùng JSONLint.com)
- Đảm bảo có đủ field title_vi/title_en và content_vi/content_en
- Kiểm tra encoding file (phải UTF-8)

### IPA không hiển thị
- Đảm bảo eng-to-ipa được cài đúng: `pip list | grep eng-to-ipa`
- Xóa cache: `DELETE FROM article_cache;`
- Restart app

## ��� Roadmap

- [ ] API REST đầy đủ
- [ ] Authentication
- [ ] Categories management
- [ ] Full-text search
- [ ] Export PDF
- [ ] Mobile app

## ��� License

MIT License - Free to use and modify

## ��� Contributing

Pull requests are welcome!

---

**Created with ❤️ for language learners**
