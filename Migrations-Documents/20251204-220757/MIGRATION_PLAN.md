# Migration Plan: Thêm hỗ trợ Tiếng Nhật (content_jp)

## Ngày: 2024-12-04

## Mục tiêu

1. Thêm trường `content_jp` vào database và logic import
2. Thêm nút "Tiếng Nhật" ở trang article
3. Cho phép chọn ngôn ngữ bên trái/phải trong chế độ song ngữ
4. Lưu tất cả settings vào localStorage

## Các file đã thay đổi

### 1. `app.py`

- [x] Thêm migration column `content_jp` và `title_jp` vào articles table
- [x] Cập nhật route import để lưu content_jp và title_jp
- [x] Database migration tự động khi khởi động

### 2. `templates/article.html`

- [x] Thêm nút "🇯🇵 日本語" vào language selector
- [x] Thêm content section cho tiếng Nhật (content-jp)
- [x] Cập nhật bilingual mode để cho phép chọn ngôn ngữ trái/phải
- [x] Thêm dropdown chọn ngôn ngữ cho mỗi cột (click vào header)
- [x] Lưu/restore settings từ localStorage (bilingualLeftLang, bilingualRightLang)
- [x] Hidden content storage để switch nội dung động

## Tiến độ

- [x] Đọc và hiểu cấu trúc hiện tại
- [x] Cập nhật database schema
- [x] Cập nhật import logic
- [x] Cập nhật giao diện article
- [x] Test và kiểm tra

## Cách sử dụng

### Import JSON với tiếng Nhật
```json
{
  "title_vi": "Tiêu đề tiếng Việt",
  "title_en": "English Title",
  "title_jp": "日本語タイトル",
  "content_vi": "<p>Nội dung tiếng Việt</p>",
  "content_en": "<p>English content</p>",
  "content_jp": "<p>日本語コンテンツ</p>",
  "category": "tech"
}
```

### Chế độ Song Ngữ
- Click vào header của cột để chọn ngôn ngữ
- Có thể chọn bất kỳ tổ hợp: VN-EN, VN-JP, EN-JP, hoặc cùng ngôn ngữ
- Settings được lưu vào localStorage

## LocalStorage Keys

- `bilingualLeftLang`: Ngôn ngữ cột trái (vi/en/jp)
- `bilingualRightLang`: Ngôn ngữ cột phải (vi/en/jp)
- `preferredLang`: Ngôn ngữ mặc định khi xem bài
