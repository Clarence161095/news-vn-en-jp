# 📚 Web App Đọc Báo Song Ngữ (Việt - Anh - Nhật)

Ứng dụng web Flask để đọc báo song ngữ với hỗ trợ tự động tạo **IPA (International Phonetic Alphabet)** cho tiếng Anh và **Furigana** cho tiếng Nhật.

## ✨ Tính năng chính

### 🌐 Đa ngôn ngữ

- **3 ngôn ngữ**: Tiếng Việt, English, 日本語
- **Chế độ song ngữ**: Xem Việt-Anh song song
- **Chuyển đổi linh hoạt**: Chuyển đổi ngôn ngữ ngay trong trang bài viết

### 🎯 Tự động tạo phiên âm

- **IPA cho tiếng Anh**: Tự động tạo phiên âm IPA với thư viện `eng-to-ipa`
- **Furigana cho tiếng Nhật**: Tự động tạo Furigana với thư viện `pykakasi`
- **Katakana → English**: Tự động dịch Katakana sang tiếng Anh với Google Translate API
- **Hiển thị Ruby tag**: Sử dụng thẻ HTML `<ruby>` chuẩn để hiển thị phiên âm

### ⚡ Hiệu năng cao

- **Multi-tier caching**: 4 tầng cache (Memory + JSON + Google Translate)
- **SQLite cache**: Lưu cache vào database thay vì RAM (tiết kiệm tài nguyên server)
- **Persistent cache**: Cache tồn tại qua các lần restart
- **Auto-cleanup**: Cache tự động xóa khi xóa bài viết (CASCADE constraint)
- **2,088 từ Katakana**: Pre-cached trong `katakana_cache.json`

### 💾 Quản lý dữ liệu

- **SQLite Database**: 2 bảng (`articles` + `article_cache`)
- **Import JSON**: Import hàng loạt từ file JSON
- **API Endpoint**: REST API để lấy dữ liệu

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# hoặc: venv\Scripts\activate  # Windows CMD
# hoặc: source venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**

- `Flask==3.0.0` - Web framework
- `Werkzeug==3.0.1` - WSGI utilities
- `pykakasi==2.2.1` - Japanese text processing (Furigana)
- `eng-to-ipa==0.0.2` - English to IPA conversion
- `deep-translator==1.11.4` - Google Translate API wrapper
- `gunicorn==21.2.0` - Production WSGI server

### 4. Chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ chạy tại: <http://localhost:5000>

## 📖 Hướng dẫn sử dụng

### Import dữ liệu

1. Truy cập: <http://localhost:5000/import>
2. Dán nội dung JSON vào form (xem định dạng bên dưới)
3. Nhấn **"Import Bài Viết"**
4. **IPA và Furigana sẽ được tự động tạo khi xem bài viết lần đầu**

### Đọc bài viết

1. **Trang chủ**: Danh sách tất cả bài viết
2. **Chọn ngôn ngữ**:
   - 🇻🇳 Đọc Tiếng Việt
   - 🇬🇧 Read English (with IPA)
   - 🇯🇵 日本語を読む (with Furigana)
   - 🌐 Song Ngữ (Việt-Anh)

3. **Trong trang bài viết**: Chuyển đổi ngôn ngữ bằng các nút trên cùng

### Cache và hiệu năng

- **Lần xem đầu tiên**: ~20ms (tạo IPA/Furigana + lưu cache)
- **Lần xem tiếp theo**: ~15ms (load từ SQLite cache)
- **Katakana translation**:
  - Tier 1: Memory cache (~1ms)
  - Tier 2: JSON file (2,088 words, ~5ms)
  - Tier 3: Fallback dictionary (~5ms)
  - Tier 4: Google Translate (~300ms, sau đó cached)

## 📝 Định dạng JSON

### Import một bài viết

```json
{
    "title_vi": "Học tiếng Anh qua báo",
    "title_en": "Learning English through news",
    "title_jp": "ニュースを通じて英語を学ぶ",
    "content_vi": "<p>Nội dung tiếng Việt...</p>",
    "content_en": "<p>English content here...</p>",
    "content_jp": "<p>日本語の内容はこちら...</p>",
    "category": "education"
}
```

**Lưu ý**:

- Không cần cung cấp `content_en_ipa` hay `content_jp_furigana`
- Hệ thống sẽ **tự động tạo** IPA và Furigana
- Cache sẽ lưu vào database để load nhanh lần sau

### Import nhiều bài viết

```json
[
    { ...bài viết 1... },
    { ...bài viết 2... },
    { ...bài viết 3... }
]
```

## 🏗️ Cấu trúc dự án

```text
news-vn-en-jp/
│
├── app.py                      # Flask app chính
├── requirements.txt            # Python dependencies
├── katakana_cache.json        # Cache 2,088 từ Katakana → English
├── articles.db                # SQLite database
│   ├── articles               # Bảng lưu bài viết gốc
│   └── article_cache          # Bảng lưu IPA/Furigana đã xử lý
│
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Trang chủ (danh sách bài viết)
    ├── article.html           # Trang chi tiết bài viết
    └── import.html            # Trang import JSON
```

## 🎯 Ví dụ Ruby tag

### Tiếng Anh với IPA (tự động)

Input:

```text
Hello world! This is pronunciation.
```

Output (tự động):

```html
<ruby>Hello<rt>/həˈloʊ/</rt></ruby> <ruby>world<rt>/wɜːrld/</rt></ruby>!
<ruby>This<rt>/ðɪs/</rt></ruby> <ruby>is<rt>/ɪz/</rt></ruby>
<ruby>pronunciation<rt>/prəˌnʌnsiˈeɪʃn/</rt></ruby>.
```

### Tiếng Nhật với Furigana (tự động)

Input:

```text
日本語を勉強します。
```

Output (tự động):

```html
<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>勉強<rt>べんきょう</rt></ruby>します。
```

### Katakana → English (tự động)

Input:

```text
コンピューター、インターネット
```

Output (tự động):

```text
computer, internet
```

## 🚀 Deploy lên EC2

### 1. Chuẩn bị server

```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài Python 3 và pip
sudo apt install python3 python3-pip python3-venv -y

# Cài Nginx (optional, để reverse proxy)
sudo apt install nginx -y
```

### 2. Clone và cài đặt

```bash
# Clone repository
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài dependencies
pip install -r requirements.txt
```

### 3. Chạy với Gunicorn (Production)

```bash
# Chạy app
gunicorn --bind 0.0.0.0:5000 app:app

# Hoặc chạy với nhiều workers
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### 4. Chạy dưới dạng service (systemd)

Tạo file `/etc/systemd/system/newsapp.service`:

```ini
[Unit]
Description=News App Flask
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/news-vn-en-jp
Environment="PATH=/home/ubuntu/news-vn-en-jp/venv/bin"
ExecStart=/home/ubuntu/news-vn-en-jp/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Khởi động service:

```bash
sudo systemctl daemon-reload
sudo systemctl start newsapp
sudo systemctl enable newsapp
sudo systemctl status newsapp
```

### 5. Cấu hình Nginx (Reverse Proxy)

Tạo file `/etc/nginx/sites-available/newsapp`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/ubuntu/news-vn-en-jp/static;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/newsapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Bảo mật EC2

- **Security Group**: Mở port 80 (HTTP) và 443 (HTTPS)
- **SSL Certificate**: Sử dụng Let's Encrypt (Certbot)
- **Firewall**: Cấu hình UFW

```bash
# Cài UFW
sudo apt install ufw -y

# Cấu hình
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 🔧 API Endpoints

### Lấy bài viết theo ID

```text
GET /api/article/<id>
```

Response:

```json
{
    "id": 1,
    "title_vi": "...",
    "title_en": "...",
    "content_en_ipa": "...",
    "content_jp_furigana": "..."
}
```

## 🐛 Troubleshooting

### Lỗi import libraries

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Database locked error

```bash
# Tắt tất cả processes đang dùng database
# Restart app
python app.py
```

### Cache không hoạt động

```bash
# Xóa cache và rebuild
rm articles.db
python app.py  # Database sẽ tự động tạo lại
```

## 📊 Hiệu năng

| Metric | Value |
|--------|-------|
| **First view** | ~20ms (generate + cache) |
| **Cached view** | ~15ms (DB query) |
| **RAM usage** | ~45MB (with SQLite cache) |
| **Katakana cache** | 2,088 words (85KB) |
| **DB size** | ~1MB (100 articles) |

## 📄 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón!

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Liên hệ

- **GitHub**: [@Clarence161095](https://github.com/Clarence161095)
- **Repository**: [news-vn-en-jp](https://github.com/Clarence161095/news-vn-en-jp)

---

**Chúc bạn học tập vui vẻ! 📚✨**
