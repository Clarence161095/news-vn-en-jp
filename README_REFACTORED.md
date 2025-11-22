# 📰 News Reader - Ứng dụng đọc báo Song Ngữ

Web app đọc báo, đọc sách, đọc nội dung Song Ngữ (Việt - Anh - Nhật) với **tự động tạo IPA và Furigana**.

## ✨ Tính năng

### 🎯 Core Features
- ✅ **7 chế độ đọc**: Tiếng Việt, English (IPA), 日本語 (Furigana), Việt-Anh, Việt-Nhật, Anh-Nhật, Tam Ngữ
- ✅ **Tự động tạo IPA**: Chuyển đổi tiếng Anh sang phiên âm IPA tự động
- ✅ **Tự động tạo Furigana**: Chuyển đổi Kanji sang Hiragana tự động
- ✅ **Toggle Furigana**: Bật/tắt furigana toàn bộ hoặc từng từ
- ✅ **Import JSON đơn giản**: Chỉ cần nội dung gốc, không cần IPA/Furigana
- ✅ **Xóa bài viết**: Dễ dàng quản lý nội dung

### 🔧 Refactoring quan trọng
**KHÔNG CẦN import IPA và Furigana nữa!**

Trước đây:
```json
{
  "content_en": "<p>Hello world</p>",
  "content_en_ipa": "<p><ruby>Hello<rt>/həˈloʊ/</rt></ruby> <ruby>world<rt>/wɝld/</rt></ruby></p>"
}
```

Bây giờ:
```json
{
  "content_en": "<p>Hello world</p>"
}
```
**IPA và Furigana được tạo TỰ ĐỘNG khi hiển thị!**

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/Clarence161095/news-vn-en-jp.git
cd news-vn-en-jp
```

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

**Requirements:**
```
Flask==3.0.0
Werkzeug==3.0.1
pykakasi==2.2.1      # Tạo Furigana tự động
eng-to-ipa==0.0.2    # Tạo IPA tự động
```

### 3. Chạy ứng dụng
```bash
python app.py
```

Truy cập: http://127.0.0.1:5000

## 📝 Cách sử dụng

### Import bài viết (JSON đơn giản)

1. Vào trang Import: http://127.0.0.1:5000/import
2. Paste JSON với format:

```json
[
  {
    "title_vi": "Tiêu đề tiếng Việt",
    "title_en": "English Title",
    "title_jp": "日本語タイトル",
    "content_vi": "<p>Nội dung tiếng Việt...</p>",
    "content_en": "<p>English content...</p>",
    "content_jp": "<p>日本語の内容...</p>",
    "category": "technology"
  }
]
```

**Lưu ý:** 
- ❌ KHÔNG CẦN `content_en_ipa`
- ❌ KHÔNG CẦN `content_jp_furigana`
- ✅ Chỉ cần nội dung gốc!

### Xem bài viết

Trang chủ hiển thị 7 nút cho mỗi bài viết:
- 🇻🇳 **Việt** - Chỉ tiếng Việt
- 🇬🇧 **Anh** - Tiếng Anh + IPA tự động
- 🇯🇵 **Nhật** - Tiếng Nhật + Furigana tự động
- 🇻🇳🇬🇧 **Việt-Anh** - Song ngữ Việt-Anh
- 🇻🇳🇯🇵 **Việt-Nhật** - Song ngữ Việt-Nhật
- 🇬🇧🇯🇵 **Anh-Nhật** - Song ngữ Anh-Nhật
- 🌐 **Tam Ngữ** - Hiển thị cả 3 ngôn ngữ

### Toggle Furigana

Khi xem bài viết tiếng Nhật:
- Nút 🎌 góc phải dưới: Bật/tắt tất cả Furigana
- Click vào từng từ: Bật/tắt Furigana của từ đó

### Xóa bài viết

- Trang chủ: Click nút 🗑️ **Xóa** trên mỗi bài
- Trang chi tiết: Click nút 🗑️ **Xóa bài viết** góc trên

## 🏗️ Kiến trúc

### Database Schema (Đơn giản hơn)
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title_vi TEXT,
    title_en TEXT,
    title_jp TEXT,
    content_vi TEXT,      -- Nội dung gốc
    content_en TEXT,      -- Nội dung gốc
    content_jp TEXT,      -- Nội dung gốc
    category TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**Không còn các cột:**
- ❌ `content_en_ipa` (tạo động)
- ❌ `content_jp_furigana` (tạo động)

### Xử lý tự động

```python
# Khi hiển thị bài viết
def process_article_content(article):
    # Tạo IPA tự động từ content_en
    article['content_en_ipa'] = generate_ipa_html(article['content_en'])
    
    # Tạo Furigana tự động từ content_jp
    article['content_jp_furigana'] = generate_furigana_html(article['content_jp'])
    
    return article
```

## 📦 Thư viện sử dụng

### pykakasi
- **Mục đích**: Chuyển đổi Kanji → Hiragana (Furigana)
- **Ví dụ**: `日本語` → `にほんご`

### eng-to-ipa
- **Mục đích**: Chuyển đổi English → IPA
- **Ví dụ**: `Hello` → `/həˈloʊ/`

## 📄 File mẫu

Xem `sample_simple.json` - chỉ có nội dung gốc, không có IPA/Furigana:

```json
[
  {
    "title_vi": "Học AWS cho người mới bắt đầu",
    "title_en": "AWS for Beginners",
    "title_jp": "初心者向けAWS",
    "content_vi": "<p>Nội dung tiếng Việt...</p>",
    "content_en": "<p>English content...</p>",
    "content_jp": "<p>日本語...</p>",
    "category": "technology"
  }
]
```

## 🎨 Giao diện

- **Responsive**: Hoạt động tốt trên desktop, tablet, mobile
- **Gradient buttons**: Mỗi ngôn ngữ có màu riêng
- **Ruby tags**: Hiển thị IPA và Furigana đẹp mắt
- **Toggle button**: Floating button góc phải dưới

## 🔄 So sánh Before/After

### Before (Phức tạp)
```json
{
  "content_en": "<p>Hello world</p>",
  "content_en_ipa": "<p><ruby>Hello<rt>/həˈloʊ/</rt></ruby>...</p>",
  "content_jp": "<p>こんにちは世界</p>",
  "content_jp_furigana": "<p>こんにちは<ruby>世界<rt>せかい</rt></ruby></p>"
}
```

### After (Đơn giản)
```json
{
  "content_en": "<p>Hello world</p>",
  "content_jp": "<p>こんにちは世界</p>"
}
```

**IPA và Furigana tự động tạo!**

## 📊 Performance

- **Database**: Nhẹ hơn (không lưu IPA/Furigana)
- **Import**: Nhanh hơn (ít dữ liệu)
- **Rendering**: Tạo động on-the-fly
- **Cache**: Có thể thêm cache cho performance tốt hơn

## 🚧 Roadmap

- [ ] Cache IPA/Furigana đã tạo
- [ ] Chỉnh sửa bài viết
- [ ] Search/Filter
- [ ] Export to PDF
- [ ] Dark mode

## 👨‍💻 Phát triển

```bash
# Development mode
python app.py

# Production (sử dụng gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

MIT License

---

**Made with ❤️ by Clarence**
