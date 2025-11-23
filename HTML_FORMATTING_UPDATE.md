# HTML Formatting & Font Size Controls Update

## Ngày: 24/11/2025

### ✅ Các vấn đề đã sửa

## 1. 📊 **Định dạng bảng (Tables)**

### Trước:
- Bảng không có border
- Hiển thị vỡ layout
- Không có styling

### Sau:
```css
- ✅ Border rõ ràng cho tất cả ô (1px solid #ddd)
- ✅ Header có màu gradient xanh dương đẹp mắt
- ✅ Dòng chẵn/lẻ khác màu (zebra striping)
- ✅ Hover effect khi di chuột qua dòng
- ✅ Border-radius cho góc bo tròn
- ✅ Box shadow tạo độ nổi
- ✅ Responsive: tự động scroll ngang trên mobile
```

**Tính năng:**
- Header có background gradient màu xanh
- Padding đủ rộng (12px 15px) cho dễ đọc
- Dòng chẵn màu #f8f9fa
- Hover hiệu ứng màu #e8f4f8
- Trên mobile: có scroll ngang, không bị vỡ

---

## 2. 📝 **Định dạng danh sách (Lists)**

### Trước:
- Gạch đầu dòng không rõ
- Thụt lề không đủ
- Spacing kém

### Sau:
```css
- ✅ Thụt lề đầy đủ (padding-left: 2.5em)
- ✅ Margin giữa các items (0.8em)
- ✅ Line-height thoáng (2.2)
- ✅ Hỗ trợ nested lists (ul trong ul, ol trong ol)
- ✅ Các kiểu bullet khác nhau cho mỗi cấp
```

**Kiểu gạch đầu dòng:**
- **Cấp 1 (ul):** disc (●)
- **Cấp 2 (ul ul):** circle (○)
- **Cấp 3 (ul ul ul):** square (■)

**Kiểu số:**
- **Cấp 1 (ol):** decimal (1, 2, 3...)
- **Cấp 2 (ol ol):** lower-alpha (a, b, c...)
- **Cấp 3 (ol ol ol):** lower-roman (i, ii, iii...)

---

## 3. 📏 **Chức năng tăng giảm font-size**

### Tính năng mới:

#### **3 nút điều khiển:**
1. **A+** - Tăng kích thước chữ
2. **A-** - Giảm kích thước chữ
3. **A** - Reset về mặc định (100%)

#### **Vị trí:**
- Fixed position bên phải màn hình
- Phía trên nút IPA toggle
- Desktop: bottom 100px
- Mobile: bottom 80px

#### **Phạm vi điều chỉnh:**
- Tối thiểu: **60%**
- Mặc định: **100%**
- Tối đa: **200%**
- Bước nhảy: **10%**

#### **Tính năng nâng cao:**
✅ **LocalStorage:** Lưu kích thước font, tự động load lại khi vào trang
✅ **Hiển thị tức thời:** Popup hiện % kích thước font trong 2 giây
✅ **Smooth transition:** Hiệu ứng chuyển đổi mượt mà (0.3s)
✅ **Keyboard shortcuts:**
   - `Ctrl/Cmd + +` : Tăng font
   - `Ctrl/Cmd + -` : Giảm font
   - `Ctrl/Cmd + 0` : Reset font

#### **Responsive:**
- Desktop: Nút 50x50px
- Mobile: Nút 45x45px
- Tooltip hiện khi hover
- Icon rõ ràng, dễ hiểu

---

## 4. 🎨 **Các định dạng khác**

### Blockquote (Trích dẫn):
```css
- Border trái 5px màu xanh #3498db
- Background màu #f0f7fb
- Italic text
- Padding 15px 20px
- Border-radius bo góc
```

### Code blocks:
```css
- Background #f4f4f4
- Border 1px solid #ddd
- Monospace font
- Horizontal scroll khi quá dài
- Inline code: padding nhỏ, border-radius
```

---

## 5. 📱 **Cải thiện Mobile**

### Tables:
- Tự động scroll ngang
- Touch scrolling mượt (-webkit-overflow-scrolling)
- Font nhỏ hơn (0.9em)
- Padding compact hơn (8px 10px)

### Lists:
- Padding-left giảm xuống 1.5em
- Giữ được cấu trúc nested

### Font controls:
- Nút nhỏ hơn (45x45px)
- Vị trí điều chỉnh phù hợp mobile
- Tooltip vẫn hoạt động tốt

---

## 🎯 **Cách sử dụng**

### Tăng/Giảm font:
1. **Cách 1:** Click vào nút A+, A-, A ở bên phải
2. **Cách 2:** Dùng phím tắt:
   - Windows: `Ctrl + +`, `Ctrl + -`, `Ctrl + 0`
   - Mac: `Cmd + +`, `Cmd + -`, `Cmd + 0`

### Lưu ý:
- Font size được lưu tự động
- Áp dụng cho tất cả nội dung bài viết
- Hoạt động cả 3 chế độ: Tiếng Việt, English, Song Ngữ
- Tự động re-align khi thay đổi font trong chế độ song ngữ

---

## 📋 **CSS Classes Added**

### Tables:
```css
.article-content table { }
.article-content table th { }
.article-content table td { }
.article-content table tr:nth-child(even) { }
.article-content table tr:hover { }
```

### Lists:
```css
.article-content ul { }
.article-content ol { }
.article-content ul ul { }
.article-content ol ol { }
.article-content ul li { }
.article-content ol li { }
```

### Font Controls:
```css
.font-controls { }
.font-btn { }
.font-size-display { }
.font-size-display.show { }
```

### Other Elements:
```css
.article-content blockquote { }
.article-content pre { }
.article-content code { }
```

---

## 🔧 **JavaScript Functions Added**

```javascript
increaseFontSize()      // Tăng font +10%
decreaseFontSize()      // Giảm font -10%
resetFontSize()         // Reset về 100%
applyFontSize()         // Áp dụng font size
loadFontSize()          // Load từ localStorage
```

---

## 🌟 **Demo**

### Bảng sẽ hiển thị như thế này:
```
┌─────────────────────────────────────────┐
│  Header 1  │  Header 2  │  Header 3    │ ← Gradient xanh
├────────────┼────────────┼──────────────┤
│  Cell 1    │  Cell 2    │  Cell 3      │ ← Màu trắng
├────────────┼────────────┼──────────────┤
│  Cell 4    │  Cell 5    │  Cell 6      │ ← Màu xám nhạt
└─────────────────────────────────────────┘
```

### Danh sách:
```
● Item 1
  ○ Nested item 1.1
    ■ Nested item 1.1.1
  ○ Nested item 1.2
● Item 2

1. First item
   a. Nested first
      i. Deeply nested
   b. Nested second
2. Second item
```

---

## ✨ **Kết quả**

✅ Bảng có border rõ ràng, đẹp mắt
✅ Danh sách thụt lề đúng, gạch đầu dòng rõ ràng
✅ Font-size tùy chỉnh dễ dàng với 3 nút
✅ Lưu settings tự động
✅ Phím tắt tiện lợi
✅ Responsive hoàn hảo trên mobile
✅ Smooth animations
✅ Professional UI/UX

---

## 📦 **Files Modified**

1. `templates/article.html` - Cập nhật toàn bộ CSS và JavaScript

## 🔄 **Compatibility**

- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari (Desktop & iOS)
- ✅ Mobile browsers
- ✅ Tablets

## 🎨 **Color Scheme**

- **Font buttons:** Red gradient (#e74c3c → #c0392b)
- **IPA button:** Blue gradient (#3498db → #2980b9)
- **Table header:** Blue gradient
- **Hover effects:** Light blue (#e8f4f8)
