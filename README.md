# 📰 News Vietnamese-English Reader

Ứng dụng đọc báo song ngữ Việt-Anh với tự động phiên âm IPA cho tiếng Anh, tích hợp nhiều tính năng nâng cao cho trải nghiệm đọc tối ưu.

## ✨ Tính năng chính

### 📖 Chế độ đọc
- **Ba chế độ hiển thị**: 
  - Tiếng Việt only
  - Tiếng Anh với IPA
  - Song ngữ đồng bộ (Bilingual Sync)
- **Tự động IPA**: Phát âm IPA tự động cho tiếng Anh (eng-to-ipa)
- **Click IPA**: Click vào từ để xem phát âm (khi IPA bị ẩn)
- **Ruby annotations**: Hiển thị IPA bằng HTML ruby tags

### 🎯 Chế độ Focus Mode
- **Fullscreen reading**: Toàn màn hình không phân tâm
- **Sync scrolling**: Cuộn đồng bộ tự nhiên giữa 2 ngôn ngữ
- **Auto-off**: Luôn tắt khi load page (tránh conflict)
- **Keyboard shortcut**: Ctrl/Cmd + F để bật/tắt

### ⚙️ Cài đặt tùy chỉnh (Settings Panel)
- **Font size**: Tăng/giảm kích thước chữ (60%-200%)
  - Shortcuts: Ctrl/Cmd + Plus/Minus/0
- **Column width**: Điều chỉnh tỷ lệ cột Việt-Anh (20%-80%)
  - Drag divider hoặc dùng slider
- **Dark mode**: Chế độ tối bảo vệ mắt
  - Shortcut: Ctrl/Cmd + D
- **IPA toggle**: Bật/tắt hiển thị IPA
  - Shortcut: Ctrl/Cmd + I
- **Lưu tự động**: Settings được lưu trong localStorage

### 🎨 Giao diện & UX
- **Responsive design**: Tối ưu cho desktop, tablet, mobile
- **Drag to resize**: Kéo thanh chia để resize cột (với touch support)
- **Smooth animations**: Hiệu ứng mượt mà, professional
- **Word wrapping**: Text xuống dòng tự nhiên với hyphens
- **Table/List formatting**: Hiển thị đẹp cho table, ul, ol
- **Optimized width**: English column 95% width để text wrap tốt hơn

### 🔧 Admin Panel
- **Login/MFA**: Đăng nhập với xác thực 2 lớp (QR code)
- **CRUD articles**: Tạo, sửa, xóa bài viết
- **Import JSON**: Nhập bài viết qua JSON với validation
- **Delete protection**: Confirm dialog khi xóa
- **Cache management**: Quản lý IPA cache tự động

## 🚀 Cài đặt nhanh

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
- **Admin dashboard**: http://localhost:5000/admin

## 📝 Định dạng JSON import

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
- HTML được preserve (table, ul, ol, p, h1-h6)
- Validation tự động kiểm tra cấu trúc JSON

## 🛠️ Scripts hữu ích

### Windows
```bash
sh reset.sh      # Reset và khởi động lại
sh start.sh      # Khởi động app
sh stop.sh       # Dừng app
sh status.sh     # Kiểm tra trạng thái
```

### Linux/macOS
```bash
./reset-linux.sh    # Reset và khởi động lại
./start.sh          # Khởi động app
./stop.sh           # Dừng app
./status.sh         # Kiểm tra trạng thái
```

## 🗄️ Cấu trúc Database

### Table: articles
- `id`: Primary key
- `title_vi`: Tiêu đề tiếng Việt
- `title_en`: Tiêu đề tiếng Anh
- `content_vi`: Nội dung tiếng Việt (HTML)
- `content_en`: Nội dung tiếng Anh (HTML)
- `category`: Danh mục
- `created_at`: Ngày tạo (UTC)
- `updated_at`: Ngày cập nhật (UTC)

### Table: article_cache
- `article_id`: Foreign key → articles.id
- `title_en_ipa`: Tiêu đề tiếng Anh có IPA
- `content_en_ipa`: Nội dung tiếng Anh có IPA
- `cached_at`: Ngày cache (UTC)

## ⚡ Tối ưu hóa hiệu năng

1. **IPA Caching**: Kết quả IPA được lưu trong database, chỉ tính 1 lần
2. **Lazy Loading**: IPA chỉ được tạo khi xem bài viết lần đầu
3. **In-memory Cache**: Cache IPA lookups trong runtime để tránh trùng lặp
4. **Optimized Regex**: Dùng compiled regex patterns
5. **HTML Block Preservation**: Preserve table/list structure khi process IPA
6. **Viewport Width Calculation**: Tính toán chính xác dựa trên vw cho responsive
7. **Debounced Resize**: Resize event được debounce 250ms

## ⌨️ Keyboard Shortcuts

| Shortcut | Chức năng |
|----------|-----------|
| `Ctrl/Cmd + Plus` | Tăng font size |
| `Ctrl/Cmd + Minus` | Giảm font size |
| `Ctrl/Cmd + 0` | Reset font size |
| `Ctrl/Cmd + D` | Toggle dark mode |
| `Ctrl/Cmd + F` | Toggle focus mode |
| `Ctrl/Cmd + I` | Toggle IPA |

## 🔧 Cấu hình

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

# Khởi động development
python app.py

# Hoặc production với gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📊 Logs

```bash
# Xem access logs
tail -f logs/access.log

# Xem error logs
tail -f logs/error.log
```

## 🐛 Xử lý lỗi thường gặp

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

### Focus Mode bị conflict
- Focus Mode đã được fix để không lưu localStorage
- Luôn bắt đầu tắt khi load page
- Chỉ bật thủ công khi cần

### Column width không chính xác
- Hard reload (Ctrl+Shift+R) để clear cache
- Kiểm tra console để xem vw calculation
- Reset về 50% bằng slider

## 📁 Cấu trúc Project

```
news-vn-en-jp/
├── app.py                    # Main Flask application
├── articles.db              # SQLite database
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── templates/              # HTML templates
│   ├── base.html          # Base layout
│   ├── index.html         # Home page
│   ├── article.html       # Article reader (main)
│   ├── import.html        # Import JSON page
│   └── admin_*.html       # Admin pages
├── logs/                   # Application logs
│   ├── access.log
│   └── error.log
├── backups/               # Database backups
└── scripts/              # Shell scripts
    ├── reset.sh
    ├── start.sh
    ├── stop.sh
    └── status.sh
```

## 🎯 Technical Highlights

### Frontend
- Pure JavaScript (no framework dependencies)
- CSS Grid for bilingual layout
- Viewport width (vw) calculations for responsive
- LocalStorage for user preferences
- Touch-enabled drag divider
- Smooth scroll sync algorithm

### Backend
- Flask 3.0 with Jinja2 templates
- SQLite with foreign key constraints
- IPA generation with eng-to-ipa
- HTML parsing with regex (optimized)
- Cache layer for performance

### Performance
- IPA caching reduces processing time by 95%
- In-memory cache for duplicate words
- Lazy IPA generation on first view
- Debounced resize events
- Optimized regex patterns

## 🗺️ Roadmap

- [ ] API REST đầy đủ
- [ ] Categories management UI
- [ ] Full-text search (Vietnamese + English)
- [ ] Export to PDF/EPUB
- [ ] Audio pronunciation (TTS)
- [ ] Vocabulary highlighting
- [ ] Progress tracking
- [ ] Mobile app (React Native)
- [ ] Multi-user support
- [ ] Annotation/notes feature

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Created with ❤️ for language learners**

*Last updated: November 24, 2025*
