# 📰 News VN-EN-JP - Ứng dụng Đọc Báo Song Ngữ

Ứng dụng web đọc báo song ngữ Việt-Anh với tính năng IPA (International Phonetic Alphabet), hỗ trợ học ngôn ngữ hiệu quả.

---

## 🎯 Tính Năng Chính

### 1. **Đọc Báo Song Ngữ**
- 🇻🇳 Hiển thị tiếng Việt
- 🇬🇧 Hiển thị tiếng Anh với IPA tự động
- 🌍 Chế độ song ngữ (Việt-Anh-IPA cùng lúc)
- ⚡ IPA được tạo tự động khi xem bài (không lưu trong JSON)
- 💾 Cache IPA trong database (tự động xóa cache > 30 ngày)

### 2. **Hệ Thống User Profile**
- 👤 Đặt tên người dùng (lưu trong localStorage)
- 📁 Mỗi user có category riêng (tự động tạo khi favorite bài viết)
- ❤️ Favorite bài viết theo từng user
- 🔒 Chỉ creator mới xóa được bài viết của mình
- 🗑️ Nút xóa chỉ hiện với bài viết của user hiện tại

### 3. **Quản Lý Category (Multi-Category)**
- 📂 Mỗi bài viết có thể có **nhiều categories**
- 🏷️ Categories hiển thị dạng tags màu sắc
- 🔍 Filter theo nhiều categories cùng lúc
- ✅ Checkbox "👤 Bài viết của [username]" - auto filter bài của user
- 🎨 UI category dropdown với checkbox

### 4. **Tìm Kiếm & Filter**
- 🔎 Tìm kiếm thông thường (LIKE)
- 🎯 Tìm kiếm Regex (nâng cao)
- 📁 Filter theo categories (multi-select)
- ⭐ Filter chỉ bài viết yêu thích
- 👤 Filter bài viết của user hiện tại

### 5. **Phân Trang (Pagination)**
- 📄 Hiển thị 20 bài viết/trang
- ⚡ Tăng performance khi có nhiều bài viết
- 🔢 Navigation: Đầu | Trước | 1 2 3 ... | Tiếp | Cuối
- 🔗 Giữ nguyên filter khi chuyển trang
- 📊 Hiển thị: "Trang X/Y (Tổng Z bài viết)"

### 6. **Import JSON**
- 📥 Import 1 hoặc nhiều bài viết cùng lúc
- 🔐 Bắt buộc có username trước khi import
- 📂 Auto add 2 categories: username + JSON category
- ✅ Backup logic đảm bảo username category luôn được add
- 📝 Hỗ trợ HTML trong content

### 7. **Dark Mode**
- 🌙 Chế độ tối bảo vệ mắt
- 💾 Lưu preference trong localStorage
- 🎨 UI tối ưu cho cả sáng/tối

---

## 🚀 Cài Đặt & Chạy

### Yêu Cầu
- Python 3.8+
- pip

### Cài Đặt Thư Viện

```bash
# Tạo virtual environment (recommended)
python -m venv venv

# Kích hoạt venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Chạy Ứng Dụng

```bash
# Development mode (debug ON)
python app.py

# Hoặc dùng script
bash start.sh

# Background mode
bash start-background.sh
```

Server sẽ chạy tại: **http://localhost:5000** hoặc **http://192.168.1.8:5000**

### Dừng Server

```bash
# Dừng server
bash stop.sh

# Check status
bash status.sh

# Reset database (XÓA TẤT CẢ DỮ LIỆU!)
bash reset.sh
```

---

## 📝 Hướng Dẫn Sử Dụng

### 1. Đặt Tên User (BẮT BUỘC trước khi import)

1. Click biểu tượng **👤** ở góc phải
2. Nhập tên của bạn (ví dụ: "Clarence")
3. Click **Lưu**
4. Tên sẽ hiển thị: "👤 Xin chào, **Clarence**!"

> ⚠️ **LƯU Ý**: Phải đặt tên trước khi import, nếu không bạn sẽ **không thể xóa** bài viết sau này!

### 2. Import Bài Viết

**Truy cập:** http://localhost:5000/import

**Định dạng JSON đơn:**
```json
{
  "title_vi": "Tiêu đề tiếng Việt",
  "title_en": "English Title",
  "content_vi": "Nội dung tiếng Việt...",
  "content_en": "English content...",
  "category": "news"
}
```

**Import nhiều bài cùng lúc:**
```json
[
  {
    "title_vi": "Bài viết 1",
    "title_en": "Article 1",
    "content_vi": "Nội dung 1",
    "content_en": "Content 1",
    "category": "technology"
  },
  {
    "title_vi": "Bài viết 2",
    "title_en": "Article 2",
    "content_vi": "Nội dung 2",
    "content_en": "Content 2",
    "category": "education"
  }
]
```

**Kết quả:**
- Bài viết sẽ có **2 categories**: Username (Clarence) + JSON category (news/technology/etc)
- IPA tự động tạo khi xem bài (không cần thêm vào JSON)
- Bạn có thể xóa bài vì có category của mình

### 3. Xem & Tìm Kiếm Bài Viết

**Homepage:** http://localhost:5000/

**Search:**
- Nhập từ khóa vào ô tìm kiếm
- ☑️ Check **"Regex"** để dùng regular expression
- Click **🔍 Tìm kiếm**

**Filter:**
- Click **📁 Categories** → Chọn categories muốn filter
- ☑️ Check **"⭐ Chỉ yêu thích"** → Chỉ hiện bài đã favorite
- ☑️ Check **"👤 Bài viết của [username]"** → Chỉ hiện bài của bạn

**Pagination:**
- Click số trang để chuyển trang
- Click **⏮️ Đầu** / **⏭️ Cuối** để nhảy nhanh
- Mỗi trang hiển thị 20 bài viết

### 4. Đọc Bài Viết

**Từ homepage, click:**
- **🇻🇳 Việt** → Chỉ tiếng Việt
- **🇬🇧 Anh** → Tiếng Anh + IPA
- **🌍 Song Ngữ** → Việt-Anh-IPA cùng lúc

**Trong trang chi tiết:**
- Click **❤️** để favorite/unfavorite
- Click **🗑️ Xóa** (chỉ hiện nếu bài của bạn)
- Xem categories của bài viết (tags màu)

### 5. Quản Lý Favorites

**Thêm favorite:**
- Click **🤍** → Chuyển thành **❤️**
- Tự động thêm username category vào bài viết

**Bỏ favorite:**
- Click **❤️** → Chuyển về **🤍**
- Category username vẫn giữ nguyên (không tự xóa)

**Xem tất cả favorites:**
- Check ☑️ **"⭐ Chỉ yêu thích"** trên homepage

### 6. Xóa Bài Viết

**Điều kiện:**
- Bài viết phải có category = username của bạn
- Nút **🗑️ Xóa** chỉ hiện với bài viết của bạn

**Cách xóa:**
1. Vào trang chi tiết bài viết hoặc từ homepage
2. Click **🗑️ Xóa**
3. Xác nhận → Bài viết bị xóa vĩnh viễn

> ⚠️ **Lưu ý**: Không thể khôi phục sau khi xóa!

---

## 🗃️ Database Schema

### Tables

**1. articles** - Lưu nội dung bài viết
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_vi TEXT,
    title_en TEXT,
    content_vi TEXT,
    content_en TEXT,
    category TEXT,              -- Legacy field (không dùng nữa)
    is_favorite INTEGER DEFAULT 0,  -- Legacy (không dùng nữa)
    created_by TEXT,            -- Username của người tạo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**2. categories** - Danh sách categories
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**3. article_categories** - Quan hệ many-to-many
```sql
CREATE TABLE article_categories (
    article_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
```

**4. user_favorites** - Favorites theo user
```sql
CREATE TABLE user_favorites (
    username TEXT NOT NULL,
    article_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, article_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);
```

**5. article_cache** - Cache IPA đã generate
```sql
CREATE TABLE article_cache (
    article_id INTEGER PRIMARY KEY,
    title_en_ipa TEXT,
    content_en_ipa TEXT,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);
```

---

## 🛠️ API Endpoints

### Articles

**GET /** - Homepage với pagination
- Query params: `page`, `q`, `regex`, `categories[]`, `favorites`

**GET /article/<id>** - Chi tiết bài viết
- Query param: `lang` (vi/en/both)

**DELETE /article/delete/<id>** - Xóa bài viết
- Body: `{"username": "..."}`
- Chỉ creator mới xóa được

**POST /import** - Import JSON
- Form data: `json_data`, `username`

### Favorites

**POST /api/article/<id>/favorite** - Toggle favorite
- Body: `{"username": "...", "is_favorite": true/false}`

**GET /api/user/<username>/favorites** - Lấy danh sách favorite IDs
- Response: `{"favorite_ids": [1, 2, 3]}`

### Categories

**GET /api/article/<id>/categories** - Lấy categories của bài viết
- Response: `{"categories": [{"id": 1, "name": "news"}, ...]}`

**POST /api/article/<id>/categories** - Update categories
- Body: `{"categories": ["news", "technology"]}`
- Thay thế toàn bộ categories

**POST /api/article/<id>/add-category** - Thêm 1 category (backup)
- Body: `{"category": "Clarence"}`
- Chỉ thêm, không xóa existing

---

## 📂 Cấu Trúc Thư Mục

```
news-vn-en-jp/
├── app.py                  # Flask application chính
├── import_logic.py         # Logic thêm categories khi import
├── articles.db             # SQLite database
├── requirements.txt        # Python dependencies
├── README.md               # Tài liệu này
│
├── templates/              # Jinja2 templates
│   ├── base.html          # Base template với header/footer
│   ├── index.html         # Homepage với search/filter/pagination
│   ├── article.html       # Chi tiết bài viết
│   ├── import.html        # Import JSON form
│   ├── admin_login.html   # Admin login (nếu enable)
│   └── ...
│
├── logs/                   # Server logs
│   ├── access.log
│   └── error.log
│
├── backups/               # Database backups (tạo bởi reset.sh)
│
├── venv/                  # Python virtual environment
│
├── Lib/                   # External libraries (eng_to_ipa)
│   └── site-packages/
│       └── eng_to_ipa/
│
└── Scripts/               # Shell scripts
    ├── start.sh           # Start server
    ├── stop.sh            # Stop server
    ├── status.sh          # Check server status
    ├── reset.sh           # Reset database
    ├── deploy.sh          # Deploy script
    └── update.sh          # Update script
```

---

## 🔧 Cấu Hình

### Flask Settings (app.py)

```python
# Secret key (THAY ĐỔI trong production!)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production-2024'

# Cache expiration (ngày)
CACHE_EXPIRATION_DAYS = 30  # Tự động xóa cache > 30 ngày

# Debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Database Location

- Development: `./articles.db`
- Backups: `./backups/articles_reset_backup_YYYYMMDD_HHMMSS.db`

---

## 🐛 Troubleshooting

### 1. Import không add category đúng

**Triệu chứng:** Bài viết chỉ có username category, không có JSON category

**Nguyên nhân:** Flask code caching

**Giải pháp:**
```bash
# Kill tất cả Python processes
ps aux | grep python | awk '{print $2}' | xargs kill -9

# Clear cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Restart server
bash start.sh
```

**Check logs:**
- Phải thấy: `✅ Article X now has categories: username, json_category`
- Nếu thấy: `⚠️ BACKUP: Force adding...` → Backup logic đã chạy

### 2. Không thấy nút Xóa

**Nguyên nhân:** 
- Chưa đặt username → Click 👤 để đặt tên
- Bài viết không có category của bạn → Import lại với username đúng

**Check:**
```sql
-- Check categories của bài viết
SELECT c.name FROM categories c
JOIN article_categories ac ON c.id = ac.category_id
WHERE ac.article_id = 1;  -- Thay 1 = article ID
```

### 3. IPA không hiển thị

**Nguyên nhân:** Library `eng-to-ipa` chưa cài

**Giải pháp:**
```bash
pip install eng-to-ipa
```

**Verify:**
- Vào http://localhost:5000/import
- Check "Trạng thái thư viện"
- Phải hiện: **IPA (eng-to-ipa): Đã cài đặt ✓**

### 4. Database bị lỗi

**Reset toàn bộ (XÓA TẤT CẢ DỮ LIỆU!):**
```bash
bash reset.sh
```

**Restore từ backup:**
```bash
# List backups
ls -lh backups/

# Copy backup về
cp backups/articles_reset_backup_20241124_120000.db articles.db
```

### 5. Pagination không hiện

**Nguyên nhân:** Có < 20 bài viết

**Kiểm tra:**
```bash
sqlite3 articles.db "SELECT COUNT(*) FROM articles;"
```

**Import thêm bài viết để test pagination**

---

## 📊 Performance Tips

### 1. Cache IPA
- IPA tự động cache trong database
- Chỉ generate 1 lần, dùng lại nhiều lần
- Auto cleanup cache > 30 ngày

### 2. Pagination
- Mỗi trang chỉ load 20 bài
- Database dùng `LIMIT` và `OFFSET`
- Nhanh ngay cả với 1000+ bài viết

### 3. Index Database
```sql
-- Tạo index để tăng tốc query
CREATE INDEX IF NOT EXISTS idx_articles_created_at ON articles(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_created_by ON articles(created_by);
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
CREATE INDEX IF NOT EXISTS idx_user_favorites_username ON user_favorites(username);
```

### 4. Production Deployment

**Dùng Gunicorn (production WSGI server):**
```bash
# Install
pip install gunicorn

# Run
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Dùng Nginx (reverse proxy):**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔒 Security Notes

### Production Checklist

- [ ] Đổi `SECRET_KEY` trong `app.py`
- [ ] Disable `debug=True` trong production
- [ ] Dùng HTTPS (SSL/TLS)
- [ ] Backup database định kỳ
- [ ] Restrict admin routes (nếu enable admin)
- [ ] Set proper file permissions (chmod 600 articles.db)
- [ ] Use environment variables cho sensitive data

### Example: Environment Variables

```python
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-do-not-use')
DATABASE = os.environ.get('DATABASE_PATH', './articles.db')
```

---

## 📈 Roadmap (Future Features)

- [ ] User authentication (login/register)
- [ ] Rich text editor cho import
- [ ] Export bài viết ra PDF/DOCX
- [ ] Thêm ngôn ngữ thứ 3 (tiếng Nhật)
- [ ] Audio pronunciation (TTS)
- [ ] Vocabulary flashcards
- [ ] Reading progress tracking
- [ ] Social features (share, comment)
- [ ] Mobile app (React Native)
- [ ] AI-powered translation suggestions

---

## 📜 License

MIT License - Free to use and modify

---

## 👥 Contributors

- **Clarence** - Initial work & main developer
- **AI Assistant** - Code implementation & documentation

---

## 📞 Support

- **Issues:** GitHub Issues
- **Docs:** This README
- **Email:** [your-email@example.com]

---

## 🎉 Changelog

### Version 2.0 (2024-11-24)
- ✅ Multi-category system (many-to-many)
- ✅ User profile with localStorage
- ✅ Per-user favorites
- ✅ Conditional delete (only creator)
- ✅ Smart delete button visibility
- ✅ Pagination (20 articles/page)
- ✅ Backup category logic for import
- ✅ "My Articles" checkbox filter
- ✅ Category tags UI

### Version 1.0 (Initial)
- ✅ Basic article reading
- ✅ IPA generation
- ✅ Search & filter
- ✅ Import JSON
- ✅ Dark mode
- ✅ Favorites (global)

---

**Enjoy reading! 📚✨**
