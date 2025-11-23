# Focus Mode & Content Display Fixes

## Các vấn đề đã sửa / Issues Fixed

### 1. ✅ Focus Mode - Chỉ hiển thị bilingual-sync-container

**Vấn đề**: Ở chế độ focus mode, các phần tử khác (header, footer, title, etc.) vẫn hiển thị.

**Giải pháp**:

- Thêm CSS để ẩn tất cả các thẻ con trực tiếp của `.card` ngoại trừ `.bilingual-sync-container`
- Ẩn `.bilingual-header` (tiêu đề cột Tiếng Việt/English)
- Ẩn `.lang-selector` (nút chọn ngôn ngữ)
- Ẩn các `.content-section` khác ngoại trừ `#content-both`
- Chỉ giữ lại `bilingual-sync-container` để đọc nội dung

```css
body.focus-mode .card > div:not(.bilingual-sync-container),
body.focus-mode .bilingual-header,
body.focus-mode .lang-selector,
body.focus-mode .content-section:not(#content-both) {
    display: none !important;
}
```

### 2. ✅ Tiếng Anh không xuống dòng (Word Wrapping)

**Vấn đề**: Phần nội dung Tiếng Anh không xuống dòng khi câu quá dài, dẫn đến mất chữ.

**Giải pháp**:

- Thêm `word-wrap: break-word` cho `.bilingual-en`
- Thêm `overflow-wrap: break-word` cho `.bilingual-en`
- Thêm `white-space: normal` để đảm bảo text wrap bình thường
- Áp dụng tương tự cho `.bilingual-column`, `.bilingual-content`, và tất cả phần tử con

```css
.bilingual-en {
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

.bilingual-column {
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}

.bilingual-content p {
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
}
```

### 3. ✅ Khoảng cách chữ quá rộng (Text Spacing)

**Vấn đề**: Các chữ cách nhau quá dài do căn lề giữa (text-align: justify).

**Giải pháp**:

- Đảm bảo `text-align: left` cho tất cả nội dung
- Đặt `word-spacing: normal` để tránh spacing quá rộng
- Đặt `letter-spacing: normal` để giữ khoảng cách chữ tự nhiên
- Thêm `hyphens: auto` để tự động ngắt từ khi cần thiết

```css
.article-content {
    text-align: left;
    word-spacing: normal;
}

.bilingual-content {
    text-align: left;
    word-spacing: normal;
    letter-spacing: normal;
    hyphens: auto;
}

.bilingual-content p {
    text-align: left;
    word-spacing: normal;
    letter-spacing: normal;
}
```

### 4. ✅ Tiếng Anh bị ẩn chữ và phần xám đè lên (NEW FIX)

**Vấn đề**: Nội dung Tiếng Anh bị ẩn do background gradient và z-index conflicts.

**Giải pháp**:

- Thay đổi background gradient phức tạp thành background trắng đơn giản
- Thêm `z-index` cho `.bilingual-content` để đảm bảo nội dung hiển thị trên cùng
- Thêm `visibility: visible !important` và `opacity: 1 !important` cho tất cả nội dung
- Đơn giản hóa ruby display từ `inline-flex` thành `inline` để tránh conflict
- Force background trong focus mode để đảm bảo không có phần xám che

```css
.bilingual-column {
    background-color: transparent;
    position: relative;
    z-index: 1;
}

.bilingual-vi,
.bilingual-en {
    background: #ffffff; /* Thay vì gradient */
}

.bilingual-content {
    position: relative;
    z-index: 10;
}

.bilingual-content * {
    visibility: visible !important;
    opacity: 1 !important;
}

body.focus-mode .bilingual-column,
body.focus-mode .bilingual-vi,
body.focus-mode .bilingual-en {
    background: #ffffff !important;
}

ruby {
    display: inline; /* Thay vì inline-flex */
}
```

## Kết quả / Results

✅ **Focus Mode**: Chỉ hiển thị nội dung song ngữ, loại bỏ tất cả các phần tử khác  
✅ **English Column**: Text xuống dòng đúng cách, không bị mất chữ  
✅ **Text Spacing**: Khoảng cách chữ tự nhiên, dễ đọc hơn, cân đối hơn  
✅ **No Hidden Text**: Không còn chữ bị ẩn hay bị phần xám đè lên  
✅ **Clean Background**: Background trắng sạch, không có gradient gây nhiễu

## Cách sử dụng / Usage

1. Mở một bài viết
2. Chọn chế độ **Song Ngữ** (🇻🇳🇬🇧)
3. Nhấn nút **Focus Mode** (🎯) ở góc dưới bên trái hoặc trong Settings Panel
4. Giờ bạn chỉ thấy nội dung song ngữ VN-EN, full screen, dễ đọc

## Các tính năng được giữ nguyên trong Focus Mode

- ⚙️ Settings Button (góc trên phải trong focus mode)
- 🎯 Focus Mode Button (góc trên trái trong focus mode)
- Synchronized scrolling giữa 2 cột
- Draggable divider để điều chỉnh độ rộng cột
- Tất cả các settings (IPA, Dark Mode, Font Size, Column Width)

---

**Ngày cập nhật**: 24/11/2025 (Updated with hidden text fix)
