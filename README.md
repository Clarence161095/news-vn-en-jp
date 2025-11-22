# 📚 Web App Đọc Báo Song Ngữ (Việt - Anh - Nhật)

Ứng dụng web đơn giản để đọc báo, sách và nội dung song ngữ bằng Python Flask.

## ✨ Tính năng

- 🌐 **Đa ngôn ngữ**: Hỗ trợ đọc nội dung bằng 3 ngôn ngữ (Việt, Anh, Nhật)
- 📖 **Song ngữ**: Xem nội dung song ngữ (Việt-Anh) cạnh nhau
- 🎌 **Furigana**: Hiển thị furigana cho tiếng Nhật bằng thẻ `<ruby>`
- 🔊 **IPA**: Hiển thị phiên âm IPA cho tiếng Anh bằng thẻ `<ruby>`
- 📥 **Import JSON**: Dễ dàng import nội dung từ file JSON
- 💾 **SQLite Database**: Lưu trữ dữ liệu đơn giản và hiệu quả
- 🎨 **Giao diện đơn giản**: Thiết kế sạch sẽ, dễ sử dụng

## 🚀 Cài đặt

### 1. Clone repository (hoặc tải về)

```bash
cd "d:\01. Project\news-vn-en-jp"
```

### 2. Tạo môi trường ảo (khuyến nghị)

```bash
python -m venv venv
source venv/Scripts/activate  # Trên Windows Git Bash
# hoặc: venv\Scripts\activate  # Trên Windows CMD
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ chạy tại: **http://localhost:5000**

## 📖 Hướng dẫn sử dụng

### Import dữ liệu mẫu

1. Mở trình duyệt và truy cập: http://localhost:5000
2. Nhấn vào nút **"Import JSON"**
3. Mở file `sample_data.json` và copy nội dung
4. Dán vào form và nhấn **"Import Bài Viết"**

### Đọc bài viết

1. Tại trang chủ, bạn sẽ thấy danh sách các bài viết
2. Chọn ngôn ngữ để đọc:
   - **Đọc Tiếng Việt**: Xem bản tiếng Việt
   - **Read English**: Xem bản tiếng Anh (có IPA)
   - **Song Ngữ**: Xem song song Việt-Anh

3. Trong trang bài viết, bạn có thể chuyển đổi giữa các chế độ:
   - 🇻🇳 Tiếng Việt
   - 🇬🇧 English (IPA)
   - 🇯🇵 日本語 (Furigana)
   - 🌐 Song Ngữ

## 📝 Định dạng JSON

### Import một bài viết:

```json
{
    "title_vi": "Tiêu đề tiếng Việt",
    "title_en": "English Title",
    "title_jp": "日本語のタイトル",
    "content_vi": "<p>Nội dung tiếng Việt...</p>",
    "content_en": "<p>English content...</p>",
    "content_jp": "<p>日本語の内容...</p>",
    "content_en_ipa": "<p>English with <ruby>pronunciation<rt>/prəˌnʌnsiˈeɪʃn/</rt></ruby></p>",
    "content_jp_furigana": "<p><ruby>日本語<rt>にほんご</rt></ruby></p>",
    "category": "news"
}
```

### Import nhiều bài viết:

```json
[
    { ...bài viết 1... },
    { ...bài viết 2... }
]
```

## 🏗️ Cấu trúc dự án

```
news-vn-en-jp/
│
├── app.py                 # File Flask chính
├── requirements.txt       # Dependencies Python
├── sample_data.json      # Dữ liệu mẫu
├── articles.db           # Database SQLite (tự động tạo)
│
└── templates/
    ├── base.html         # Template cơ sở
    ├── index.html        # Trang danh sách bài viết
    ├── article.html      # Trang chi tiết bài viết
    └── import.html       # Trang import JSON
```

## 🎯 Sử dụng Ruby tag

### Tiếng Anh với IPA:

```html
<ruby>hello<rt>/həˈloʊ/</rt></ruby> <ruby>world<rt>/wɜːrld/</rt></ruby>
```

### Tiếng Nhật với Furigana:

```html
<ruby>日本語<rt>にほんご</rt></ruby>を<ruby>勉強<rt>べんきょう</rt></ruby>します。
```

## 🔧 Tính năng nâng cao

- **API Endpoint**: Truy cập `http://localhost:5000/api/article/<id>` để lấy dữ liệu JSON
- **Danh mục**: Phân loại bài viết theo category (news, book, article, v.v.)
- **Responsive**: Giao diện tự động điều chỉnh trên mobile

## 📄 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo pull request hoặc báo cáo issues.

---

**Chúc bạn học tập vui vẻ! 📚✨**