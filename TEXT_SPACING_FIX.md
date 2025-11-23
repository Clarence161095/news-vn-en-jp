# Text Spacing & Alignment Fix

## Ngày: 24/11/2025

## Vấn đề
Các chữ cách nhau quá dài, có khả năng đang căn lề justify (căn đều 2 bên) khiến text khó đọc.

## Nguyên nhân
1. **Line-height quá cao**: `line-height: 2.5` → dòng cách nhau quá xa
2. **Không có text-align: left**: Mặc định có thể là justify hoặc inherit
3. **Word-spacing không được control**: Có thể bị browser auto-adjust

## Giải pháp

### 1. Giảm Line Height từ 2.5 → 1.8
**Trước**:
```css
.article-content {
    line-height: 2.5;  /* ❌ Quá cao */
}

.article-content p {
    line-height: 2.5;  /* ❌ Quá cao */
}
```

**Sau**:
```css
.article-content {
    line-height: 1.8;  /* ✅ Vừa phải */
    text-align: left;
    word-spacing: normal;
}

.article-content p {
    line-height: 1.8;  /* ✅ Vừa phải */
    text-align: left;
    word-spacing: normal;
}
```

**Kết quả**: Dòng text gần nhau hơn, dễ đọc hơn

---

### 2. Fix Bilingual Content Spacing
**Trước**:
```css
.bilingual-content p {
    margin-bottom: 1.5em;
    line-height: 2.2;  /* ❌ Hơi cao */
}
```

**Sau**:
```css
.bilingual-content p {
    margin-bottom: 1.5em;
    line-height: 1.8;          /* ✅ Tối ưu */
    text-align: left;          /* ✅ Căn trái */
    word-spacing: normal;      /* ✅ Khoảng cách từ bình thường */
    letter-spacing: normal;    /* ✅ Khoảng cách chữ bình thường */
}

.bilingual-content {
    text-align: left;
    word-spacing: normal;
    letter-spacing: normal;
}

.bilingual-content h1,
.bilingual-content h2,
.bilingual-content h3,
.bilingual-content h4 {
    text-align: left;  /* ✅ Headers căn trái */
}
```

**Kết quả**: 
- Text căn trái (không justify)
- Khoảng cách giữa các từ bình thường
- Khoảng cách giữa các chữ bình thường

---

## Line Height Comparison

### Line-height: 2.5 (Cũ - ❌)
```
This is a sample text with line height 2.5.


It has too much space between lines.


Very hard to read for long content.
```

### Line-height: 1.8 (Mới - ✅)
```
This is a sample text with line height 1.8.

It has comfortable space between lines.

Easy to read and scan quickly.
```

---

## Text Alignment Explained

### `text-align: left`
- Căn trái, text tự nhiên
- Khoảng cách giữa từ đều nhau
- **Recommended** cho content dài

### `text-align: justify` (❌ Tránh dùng)
- Căn đều 2 bên
- Browser tự động kéo giãn khoảng cách giữa từ
- Khiến text trông lạ, khó đọc

### `text-align: center` 
- Căn giữa
- Chỉ dùng cho titles, không dùng cho paragraphs

---

## Word/Letter Spacing

### `word-spacing: normal`
- Khoảng cách giữa các từ mặc định
- Browser không tự ý thay đổi

### `letter-spacing: normal`
- Khoảng cách giữa các chữ mặc định
- Không có extra spacing

---

## CSS Properties Summary

| Property | Cũ | Mới | Lý do |
|----------|-----|-----|-------|
| `line-height` | 2.5 | 1.8 | Giảm khoảng cách dòng |
| `text-align` | - | left | Căn trái, không justify |
| `word-spacing` | - | normal | Khoảng cách từ bình thường |
| `letter-spacing` | - | normal | Khoảng cách chữ bình thường |

---

## Testing Checklist

- [x] Line height giảm từ 2.5 → 1.8
- [x] Text align left (không justify)
- [x] Word spacing normal
- [x] Letter spacing normal
- [x] Vietnamese text dễ đọc
- [x] English text dễ đọc
- [x] Headers align left
- [x] Paragraphs align left
- [x] Focus mode - spacing OK
- [x] Dark mode - spacing OK

---

## Files Modified
- `templates/article.html`
  - CSS: `.article-content` → line-height 1.8, text-align left
  - CSS: `.article-content p` → line-height 1.8, text-align left
  - CSS: `.bilingual-content` → text-align left, word-spacing normal
  - CSS: `.bilingual-content p` → line-height 1.8, text-align left
  - CSS: `.bilingual-content h1-h4` → text-align left

---

## Recommended Line Heights

| Content Type | Line Height | Usage |
|--------------|-------------|-------|
| Body text | 1.6 - 1.8 | ✅ Easy reading |
| Headers | 1.2 - 1.4 | Compact |
| Captions | 1.4 - 1.6 | Small text |
| Code | 1.5 | Monospace |
| Poetry | 2.0+ | Special formatting |

---

## Conclusion

Vấn đề text spacing đã được fix:
1. ✅ Line height: 2.5 → 1.8 (giảm 28%)
2. ✅ Text align: left (không justify)
3. ✅ Word spacing: normal
4. ✅ Letter spacing: normal

Text giờ dễ đọc hơn, tự nhiên hơn, và cân đối hơn! 🎉

**Khoảng cách giữa các từ không còn bị kéo dài**
**Dòng text không còn cách nhau quá xa**
**Tất cả content căn trái, dễ scan**
