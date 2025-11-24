# 🤖 Hướng Dẫn ChatGPT Post Bài Tự Động Hàng Ngày

## 📋 Thông Tin Hệ Thống

**Website**: http://16.176.182.214/  
**API Endpoint**: `http://16.176.182.214/api/import`  
**Phương thức**: `POST`  
**Authentication**: Không cần (Open API)  
**Content-Type**: `application/json`

---

## 🎯 Mục Đích

Sử dụng ChatGPT để tự động tạo và đăng bài viết song ngữ (Việt-Anh) hàng ngày vào hệ thống.

---

## 📝 Format JSON Chuẩn

### Đăng 1 bài viết:

```json
{
  "articles": [
    {
      "title_vi": "Tiêu đề bài viết tiếng Việt",
      "title_en": "English Article Title",
      "content_vi": "Nội dung đầy đủ bằng tiếng Việt...",
      "content_en": "Full content in English...",
      "category": "news"
    }
  ]
}
```

### Đăng nhiều bài viết cùng lúc:

```json
{
  "articles": [
    {
      "title_vi": "Bài viết số 1",
      "title_en": "Article 1",
      "content_vi": "Nội dung 1...",
      "content_en": "Content 1...",
      "category": "technology"
    },
    {
      "title_vi": "Bài viết số 2",
      "title_en": "Article 2",
      "content_vi": "Nội dung 2...",
      "content_en": "Content 2...",
      "category": "education"
    }
  ]
}
```

---

## 📂 Categories Hợp Lệ

Bạn có thể dùng bất kỳ category nào, ví dụ:

- `news` - Tin tức
- `technology` - Công nghệ
- `education` - Giáo dục
- `business` - Kinh doanh
- `health` - Sức khỏe
- `entertainment` - Giải trí
- `sports` - Thể thao
- `science` - Khoa học
- `lifestyle` - Phong cách sống
- `travel` - Du lịch
- `food` - Ẩm thực
- `book` - Sách
- `movie` - Phim
- `music` - Âm nhạc
- `gaming` - Game

**Lưu ý**: Nếu category chưa tồn tại, hệ thống sẽ tự động tạo mới.

---

## 🔧 Cách Sử Dụng với ChatGPT

### Prompt Template cho ChatGPT:

```
Bạn hãy viết cho tôi 1 bài viết song ngữ Việt-Anh về chủ đề [CHỦ ĐỀ].
Sau đó, hãy gọi API sau để đăng bài:

POST http://16.176.182.214/api/import
Content-Type: application/json

Body:
{
  "articles": [
    {
      "title_vi": "[Tiêu đề tiếng Việt]",
      "title_en": "[English Title]",
      "content_vi": "[Nội dung tiếng Việt đầy đủ]",
      "content_en": "[Full English content]",
      "category": "[CATEGORY]"
    }
  ]
}

Yêu cầu:
- Nội dung phải dài tối thiểu 300 từ mỗi ngôn ngữ
- Nội dung phải có cấu trúc rõ ràng với các đoạn văn
- Tiêu đề hấp dẫn, súc tích
- Category phù hợp với chủ đề
```

### Ví dụ Prompt Cụ Thể:

```
Viết 1 bài về "Lợi ích của việc học tiếng Anh" rồi đăng lên 
http://16.176.182.214/api/import với category "education"
```

---

## 📊 Response Format

### Thành công:

```json
{
  "success": true,
  "imported_count": 1,
  "article_ids": [42],
  "message": "Successfully imported 1 articles",
  "details": [
    {
      "article_id": 42,
      "title_vi": "Lợi ích của việc học tiếng Anh",
      "categories": ["Bot", "education"]
    }
  ]
}
```

### Lỗi - Thiếu dữ liệu:

```json
{
  "success": false,
  "error": "No articles provided"
}
```

### Lỗi - Format sai:

```json
{
  "success": false,
  "error": "Articles must be an array"
}
```

---

## 🧪 Test API bằng cURL

### Test đăng 1 bài:

```bash
curl -X POST http://16.176.182.214/api/import \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title_vi": "Test API Import",
        "title_en": "Test API Import",
        "content_vi": "Đây là bài test import qua API",
        "content_en": "This is a test article via API",
        "category": "technology"
      }
    ]
  }'
```

### Test đăng nhiều bài:

```bash
curl -X POST http://16.176.182.214/api/import \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title_vi": "Bài 1: AI và Tương Lai",
        "title_en": "Article 1: AI and Future",
        "content_vi": "Trí tuệ nhân tạo đang thay đổi thế giới...",
        "content_en": "Artificial Intelligence is changing the world...",
        "category": "technology"
      },
      {
        "title_vi": "Bài 2: Học Lập Trình",
        "title_en": "Article 2: Learning Programming",
        "content_vi": "Lập trình là kỹ năng quan trọng...",
        "content_en": "Programming is an important skill...",
        "category": "education"
      }
    ]
  }'
```

---

## 🎨 Template Bài Viết Mẫu

### Template 1: Bài Tin Tức

```json
{
  "articles": [
    {
      "title_vi": "Tiêu đề tin tức hấp dẫn",
      "title_en": "Engaging News Title",
      "content_vi": "<p>Đoạn mở đầu giới thiệu vấn đề...</p><p>Đoạn phân tích chi tiết...</p><p>Kết luận...</p>",
      "content_en": "<p>Introduction paragraph...</p><p>Detailed analysis...</p><p>Conclusion...</p>",
      "category": "news"
    }
  ]
}
```

### Template 2: Bài Hướng Dẫn

```json
{
  "articles": [
    {
      "title_vi": "Hướng dẫn chi tiết về [Chủ đề]",
      "title_en": "Complete Guide to [Topic]",
      "content_vi": "<h2>Giới thiệu</h2><p>...</p><h2>Bước 1</h2><p>...</p><h2>Bước 2</h2><p>...</p>",
      "content_en": "<h2>Introduction</h2><p>...</p><h2>Step 1</h2><p>...</p><h2>Step 2</h2><p>...</p>",
      "category": "education"
    }
  ]
}
```

### Template 3: Bài Review

```json
{
  "articles": [
    {
      "title_vi": "Đánh giá [Sản phẩm/Dịch vụ]",
      "title_en": "Review of [Product/Service]",
      "content_vi": "<h2>Tổng quan</h2><p>...</p><h2>Ưu điểm</h2><ul><li>...</li></ul><h2>Nhược điểm</h2><ul><li>...</li></ul>",
      "content_en": "<h2>Overview</h2><p>...</p><h2>Pros</h2><ul><li>...</li></ul><h2>Cons</h2><ul><li>...</li></ul>",
      "category": "technology"
    }
  ]
}
```

---

## 🤖 Automation với ChatGPT - Lịch Đăng Bài

### Lịch đề xuất:

**Thứ 2**: Technology (Công nghệ)
**Thứ 3**: Education (Giáo dục)  
**Thứ 4**: Health (Sức khỏe)
**Thứ 5**: Business (Kinh doanh)
**Thứ 6**: Lifestyle (Phong cách sống)
**Thứ 7**: Entertainment (Giải trí)
**Chủ nhật**: Travel/Food (Du lịch/Ẩm thực)

### Prompt Tự Động Hàng Ngày:

```
Hôm nay là [THỨ], hãy viết 1 bài về [CHỦ ĐỀ THEO LỊCH] 
và đăng lên http://16.176.182.214/api/import

Yêu cầu:
- Nội dung 500-800 từ mỗi ngôn ngữ
- Có hình ảnh/ví dụ minh họa (dùng HTML)
- Dễ đọc, có cấu trúc rõ ràng
- Category phù hợp
```

---

## ✅ Checklist Trước Khi Post

- [ ] Tiêu đề Việt và Anh đã có
- [ ] Nội dung Việt và Anh đầy đủ (> 300 từ)
- [ ] Category đã chọn phù hợp
- [ ] Nội dung đã format HTML (nếu cần)
- [ ] JSON format đúng chuẩn
- [ ] Test API response trước khi deploy

---

## 🔍 Debug & Troubleshooting

### Lỗi: "No JSON data provided"
→ **Fix**: Đảm bảo header `Content-Type: application/json`

### Lỗi: "No articles provided"
→ **Fix**: Đảm bảo có key `"articles"` trong JSON

### Lỗi: "Articles must be an array"
→ **Fix**: `"articles": [...]` phải là array, không phải object

### Bài viết không hiển thị category
→ **Check**: Category có trong danh sách categories của hệ thống chưa
→ **Fix**: Hệ thống tự động tạo category mới nếu chưa có

### Bài viết thiếu creator "Bot"
→ **Đây là lỗi backend**: Contact admin để fix

---

## 📞 Support

**Website**: http://16.176.182.214/  
**API Docs**: http://16.176.182.214/api/docs (nếu có)
**GitHub**: https://github.com/Clarence161095/news-vn-en-jp

---

## 🎉 Ví Dụ Hoàn Chỉnh

### Prompt cho ChatGPT:

```
Viết 1 bài về "10 Lợi Ích Của Việc Đọc Sách Hàng Ngày" 
bằng tiếng Việt và tiếng Anh, mỗi bên 600 từ.

Sau đó POST lên API này:
http://16.176.182.214/api/import

JSON format:
{
  "articles": [{
    "title_vi": "10 Lợi Ích Của Việc Đọc Sách Hàng Ngày",
    "title_en": "10 Benefits of Reading Books Daily",
    "content_vi": "[Nội dung tiếng Việt]",
    "content_en": "[English content]",
    "category": "education"
  }]
}

Hãy tạo nội dung có cấu trúc:
- Mở đầu
- 10 lợi ích (mỗi lợi ích 1 đoạn)
- Kết luận

Sau khi viết xong, gọi API và báo kết quả cho tôi.
```

### Response từ ChatGPT:

```
✅ Đã đăng bài thành công!

Kết quả:
- Article ID: 42
- Tiêu đề: "10 Lợi Ích Của Việc Đọc Sách Hàng Ngày"
- Categories: Bot, education
- Link: http://16.176.182.214/article/42

Response từ API:
{
  "success": true,
  "imported_count": 1,
  "article_ids": [42],
  "message": "Successfully imported 1 articles"
}
```

---

## 🚀 Quick Start cho ChatGPT

Copy prompt này và paste vào ChatGPT:

```
Từ bây giờ, mỗi ngày bạn sẽ viết 1 bài song ngữ Việt-Anh 
và tự động đăng lên http://16.176.182.214/api/import

Lịch đăng bài:
- Thứ 2: Technology
- Thứ 3: Education  
- Thứ 4: Health
- Thứ 5: Business
- Thứ 6: Lifestyle
- Thứ 7: Entertainment
- CN: Travel/Food

Format JSON:
{
  "articles": [{
    "title_vi": "...",
    "title_en": "...",
    "content_vi": "...",
    "content_en": "...",
    "category": "..."
  }]
}

Yêu cầu nội dung:
- 500-800 từ mỗi ngôn ngữ
- Có cấu trúc rõ ràng
- Tiêu đề hấp dẫn
- Sử dụng HTML cho format (nếu cần)

Hãy bắt đầu ngay hôm nay!
```

---

**Created by**: Clarence161095  
**Last Updated**: 2024-11-24  
**Version**: 1.0
